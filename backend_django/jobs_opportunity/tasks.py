import ipaddress
import json
import re
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
from .scraper import fetch_and_extract

# backend_django/jobs_opportunity/tasks.py
from celery import shared_task
import logging
from .scraper import JobScraperService
from .models import JobOpportunity

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='jobs_opportunity.tasks.run_job_scraper_task')
def run_job_scraper_task(self):
    """
    Asynchronous Celery task to scrape job opportunities and persist them securely into SQLite.
    """
    logger.info("Starting asynchronous job scraping task...")
    try:
        scraper = JobScraperService()
        scraped_jobs = scraper.fetch_and_parse()

        saved_count = 0
        for job_data in scraped_jobs:
            obj, created = JobOpportunity.objects.update_or_create(
                external_id=job_data.get('external_id'),
                defaults={
                    'title': job_data.get('title'),
                    'company': job_data.get('company'),
                    'location': job_data.get('location'),
                    'url': job_data.get('url'),
                    'description': job_data.get('description'),
                    'source': job_data.get('source'),
                    'is_active': True
                }
            )
            if created:
                saved_count += 1

        logger.info(
            f"Job scraping completed successfully. Added {saved_count} new jobs.")
        return {"status": "success", "new_jobs": saved_count}
    except Exception as exc:
        logger.error(f"Job scraping failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


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
                raise ValueError(
                    "Private or local network source URLs are not allowed.")
    except socket.gaierror as exc:
        raise ValueError("Source host could not be resolved.") from exc
    return url


def _skill_names(item):
    raw = item.get("skills") or item.get(
        "required_skills") or item.get("tags") or []
    if isinstance(raw, str):
        raw = [x.strip() for x in raw.split(",") if x.strip()]
    return raw if isinstance(raw, list) else []


def _canonical_key(item):
    raw_url = str(item.get("url") or item.get("link")
                  or item.get("absolute_url") or "").strip()
    if raw_url:
        parsed = urllib.parse.urlparse(raw_url)
        return urllib.parse.urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", "", ""))[:400]
    raw = "|".join([str(item.get("title") or "").strip().lower(), str(item.get("company") or item.get(
        "employer") or item.get("company_name") or "").strip().lower(), str(item.get("location") or "").strip().lower()])
    return __import__("hashlib").sha256(raw.encode("utf-8")).hexdigest()


def _upsert_job(source, item):
    external_id = str(item.get("id") or item.get("guid")
                      or item.get("external_id") or "")[:255]
    title = str(item.get("title") or item.get(
        "name") or "Untitled opportunity")[:255]
    description = str(item.get("description") or item.get(
        "summary") or item.get("content") or "")
    loc = item.get("location")
    if isinstance(loc, dict):
        loc = loc.get("name", "")
    canonical_key = _canonical_key(item)
    existing = JobOpportunity.objects.filter(
        user=source.user, canonical_key=canonical_key).first() if canonical_key else None
    defaults = {
        "title": title, "company": str(item.get("company") or item.get("employer") or item.get("company_name") or source.name)[:255],
        "description": description, "url": str(item.get("url") or item.get("link") or item.get("absolute_url") or "")[:500],
        "location": str(loc or "")[:255], "is_remote": bool(item.get("remote") or item.get("is_remote") or "remote" in str(loc or "").lower()),
        "published_at": item.get("published_at") or item.get("date") or item.get("first_published") or item.get("updated_at") or None,
        "salary_min": item.get("salary_min") or item.get("min_salary") or None, "salary_max": item.get("salary_max") or item.get("max_salary") or None,
        "currency": str(item.get("currency") or "USD")[:10],
        "job_type": item.get("job_type") if item.get("job_type") in dict(JobOpportunity.JobType.choices) else JobOpportunity.JobType.FULL_TIME,
        "canonical_key": canonical_key, "metadata": item, "is_active": True, "last_checked_at": timezone.now(),
    }
    if existing:
        for key, value in defaults.items():
            setattr(existing, key, value)
        if external_id:
            existing.external_id = external_id
        existing.source = source
        existing.save()
        job = existing
    else:
        job = JobOpportunity.objects.create(
            user=source.user, source=source, external_id=external_id, **defaults)
    for name in _skill_names(item):
        skill = Skill.objects.filter(is_active=True).filter(slug__iexact=str(name).strip()).first(
        ) or Skill.objects.filter(is_active=True, name__iexact=str(name).strip()).first()
        if skill:
            JobSkillRequirement.objects.update_or_create(job=job, skill=skill, defaults={
                                                         "required_level": item.get("required_level", "intermediate"), "importance": 1})
    JobParserService.analyze(job)
    JobMatchingService.calculate(source.user, job)
    return job


def _rss_items(content):
    """Parse RSS/Atom defensively. Invalid XML should be recorded without destroying the whole sync."""
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        # Common feeds contain unescaped HTML entities. Retry after stripping illegal control chars.
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]",
                         "", content.decode("utf-8", errors="replace"))
        try:
            root = ET.fromstring(cleaned)
        except ET.ParseError as exc:
            raise ValueError(f"RSS/Atom feed is not valid XML: {exc}") from exc
    items = []
    for node in root.findall('.//item') + root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        def val(*names):
            for name in names:
                x = node.find(name) or node.find('.//'+name)
                if x is not None and x.text:
                    return x.text.strip()
            return ''
        link = val('link', '{http://www.w3.org/2005/Atom}link')
        items.append({'id': val('guid', 'id') or link, 'title': val('title'), 'description': val(
            'description', 'summary'), 'company': val('company', 'employer'), 'location': val('location'), 'url': link})
    return items


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def sync_job_source(self, source_id):
    source = JobSource.objects.get(pk=source_id)
    source.last_sync_status = "running"
    source.last_sync_error = ""
    source.save(update_fields=["last_sync_status",
                "last_sync_error", "updated_at"])
    try:
        url = _safe_url(source.feed_url or source.base_url)
        fetch_meta = {}
        if source.source_type == JobSource.SourceType.SCRAPER:
            items, fetch_meta = fetch_and_extract(url, source.config or {
            }, user_agent="So-IAM-OS-JobScraper/1.0", rate_limit_seconds=(source.config or {}).get("rate_limit_seconds", 1))
        else:
            response = requests.get(url, timeout=20, headers={
                                    "User-Agent": "So-IAM-OS Job Sync/1.1", "Accept": "application/json,application/xml,text/xml,text/html"})
            response.raise_for_status()
            if source.source_type == JobSource.SourceType.RSS:
                items = _rss_items(response.content)
            else:
                try:
                    data = response.json()
                except ValueError:
                    data = _rss_items(response.content)
                adapter = (source.config or {}).get("adapter")
                if adapter == "greenhouse":
                    items = [{**x, "company": x.get("company_name") or source.name, "location": (x.get("location") or {}).get("name", ""), "url": x.get(
                        "absolute_url"), "description": x.get("content", ""), "published_at": x.get("first_published")} for x in (data.get("jobs", []) if isinstance(data, dict) else [])]
                elif adapter == "lever":
                    items = [{**x, "url": x.get("hostedUrl") or x.get("applyUrl"), "description": x.get("descriptionPlain") or x.get("description", ""),
                              "company": source.name, "location": (x.get("categories") or {}).get("location", "")} for x in (data if isinstance(data, list) else [])]
                elif adapter == "remotive":
                    items = data.get("jobs", []) if isinstance(
                        data, dict) else []
                elif adapter == "arbeitnow":
                    items = data.get("data", []) if isinstance(
                        data, dict) else []
                elif adapter == "jobicy":
                    items = data.get("jobs", []) if isinstance(
                        data, dict) else []
                elif isinstance(data, dict):
                    items = data.get("items") or data.get(
                        "jobs") or data.get("results") or []
                else:
                    items = data if isinstance(data, list) else []
        created = []
        with transaction.atomic():
            for item in items[: max(1, min(source.max_items_per_sync, 500))]:
                if isinstance(item, dict):
                    created.append(_upsert_job(source, item).id)
        source.last_synced_at = timezone.now()
        source.last_sync_status = "completed"
        source.last_sync_error = ""
        source.last_sync_count = len(created)
        source.save(update_fields=["last_synced_at", "last_sync_status",
                    "last_sync_error", "last_sync_count", "updated_at"])
        return {"source_id": source.id, "status": "completed", "jobs": len(created), "metadata": fetch_meta}
    except Exception as exc:
        source.last_synced_at = timezone.now()
        source.last_sync_status = "failed"
        source.last_sync_error = str(exc)[:2000]
        source.save(update_fields=[
                    "last_synced_at", "last_sync_status", "last_sync_error", "updated_at"])
        raise


@shared_task
def refresh_all_job_sources():
    ids = list(JobSource.objects.filter(
        enabled=True).values_list("id", flat=True))
    for source_id in ids:
        sync_job_source.delay(source_id)
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
    count = JobOpportunity.objects.filter(
        is_active=True, expires_at__lt=cutoff).update(is_active=False, is_expired=True)
    return count
