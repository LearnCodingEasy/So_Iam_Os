import ipaddress
import json
import socket
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from learning.models import Skill
from .models import JobSource, JobOpportunity, JobSkillRequirement
from .services import JobMatchingService, JobParserService, JobRecommendationService, JobAnalyticsService


def _safe_url(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only HTTP(S) source URLs are allowed.")
    host = parsed.hostname
    try:
        addresses = socket.getaddrinfo(host, None)
        for item in addresses:
            ip = ipaddress.ip_address(item[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError("Private or local network source URLs are not allowed.")
    except socket.gaierror as exc:
        raise ValueError("Source host could not be resolved.") from exc
    return url


def _skill_names(item):
    raw = item.get("skills") or item.get("required_skills") or item.get("tags") or []
    if isinstance(raw, str):
        raw = [x.strip() for x in raw.split(",") if x.strip()]
    return raw if isinstance(raw, list) else []


def _upsert_job(source, item):
    external_id = str(item.get("id") or item.get("guid") or item.get("external_id") or item.get("url") or "")[:255]
    title = str(item.get("title") or item.get("name") or "Untitled opportunity")[:255]
    description = str(item.get("description") or item.get("summary") or "")
    job, _ = JobOpportunity.objects.update_or_create(
        user=source.user, source=source, external_id=external_id,
        defaults={
            "title": title, "company": str(item.get("company") or item.get("employer") or "")[:255],
            "description": description, "url": str(item.get("url") or item.get("link") or "")[:500],
            "location": str(item.get("location") or "")[:255],
            "is_remote": bool(item.get("remote") or item.get("is_remote")),
            "published_at": item.get("published_at") or item.get("date") or None,
            "salary_min": item.get("salary_min") or item.get("min_salary") or None,
            "salary_max": item.get("salary_max") or item.get("max_salary") or None,
            "currency": str(item.get("currency") or "USD")[:10],
            "job_type": item.get("job_type") if item.get("job_type") in dict(JobOpportunity.JobType.choices) else JobOpportunity.JobType.FULL_TIME,
            "metadata": item,
            "is_active": True,
        }
    )
    names = _skill_names(item)
    for name in names:
        skill = Skill.objects.filter(is_active=True).filter(slug__iexact=str(name).strip()).first() or Skill.objects.filter(is_active=True, name__iexact=str(name).strip()).first()
        if skill:
            JobSkillRequirement.objects.update_or_create(job=job, skill=skill, defaults={"required_level": item.get("required_level", "intermediate"), "importance": 1})
    JobParserService.analyze(job)
    JobMatchingService.calculate(source.user, job)
    return job


def _rss_items(content):
    root = ET.fromstring(content)
    items=[]
    for node in root.findall('.//item') + root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        def val(*names):
            for name in names:
                x=node.find(name) or node.find('.//'+name)
                if x is not None and x.text: return x.text.strip()
            return ''
        link=val('link','{http://www.w3.org/2005/Atom}link')
        items.append({'id':val('guid','id') or link,'title':val('title'),'description':val('description','summary'),'company':val('company','employer'),'location':val('location'),'url':link})
    return items

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def sync_job_source(self, source_id):
    source = JobSource.objects.get(pk=source_id)
    source.last_sync_status = "running"; source.last_sync_error = ""; source.save(update_fields=["last_sync_status","last_sync_error","updated_at"])
    try:
        url = _safe_url(source.feed_url or source.base_url)
        response = requests.get(url, timeout=15, headers={"User-Agent":"So-IAM-OS Job Sync/1.0"})
        response.raise_for_status()
        if source.source_type == JobSource.SourceType.RSS:
            items = _rss_items(response.content)
        else:
            data = response.json()
            items = data.get("items") or data.get("jobs") or data.get("results") or (data if isinstance(data,list) else [])
        created=[]
        with transaction.atomic():
            for item in items[:100]:
                if isinstance(item, dict): created.append(_upsert_job(source,item).id)
        source.last_synced_at=timezone.now(); source.last_sync_status="completed"; source.last_sync_error=""; source.last_sync_count=len(created); source.save(update_fields=["last_synced_at","last_sync_status","last_sync_error","last_sync_count","updated_at"])
        return {"source_id": source.id, "status": "completed", "jobs": len(created)}
    except Exception as exc:
        source.last_synced_at=timezone.now(); source.last_sync_status="failed"; source.last_sync_error=str(exc)[:2000]; source.save(update_fields=["last_synced_at","last_sync_status","last_sync_error","updated_at"])
        raise

@shared_task
def refresh_all_job_sources():
    ids=list(JobSource.objects.filter(enabled=True).values_list("id",flat=True))
    for source_id in ids: sync_job_source.delay(source_id)
    return len(ids)


@shared_task
def refresh_all_job_matches():
    from django.contrib.auth import get_user_model
    total = 0
    for user in get_user_model().objects.filter(is_active=True):
        total += len(JobMatchingService.refresh_for_user(user))
        JobRecommendationService.refresh(user)
        JobAnalyticsService.dashboard(user)
    return total

@shared_task
def expire_old_jobs():
    cutoff = timezone.now()
    count = JobOpportunity.objects.filter(is_active=True, expires_at__lt=cutoff).update(is_active=False, is_expired=True)
    return count
