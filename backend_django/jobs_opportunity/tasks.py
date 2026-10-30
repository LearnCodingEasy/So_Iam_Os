import ipaddress
import json
import re
from datetime import datetime, time
import socket
import urllib.parse
import xml.etree.ElementTree as ET
import requests
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
from decimal import Decimal, InvalidOperation
from learning.models import Skill
from .models import JobSource, JobOpportunity, JobSkillRequirement
from .services import JobMatchingService, JobParserService, JobRecommendationService, JobAnalyticsService
from .scraper import fetch_and_extract

def _safe_url(url):
    parsed = urllib.parse.urlparse(url or "")
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only HTTP(S) source URLs are allowed.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in source URLs are not allowed.")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith((".localhost", ".local")):
        raise ValueError("Local hostnames are not allowed.")
    if parsed.port and parsed.port not in (80, 443):
        raise ValueError("Only standard HTTP/HTTPS ports are allowed.")
    try:
        addresses = {ipaddress.ip_address(item[4][0]) for item in socket.getaddrinfo(
            host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)}
        if not addresses or any(not address.is_global for address in addresses):
            raise ValueError("Private, loopback, link-local and reserved addresses are not allowed.")
    except socket.gaierror as exc:
        raise ValueError("Source host could not be resolved.") from exc
    return url


def _json_path(data, path):
    current = data
    if not path:
        return current
    for key in str(path).split("."):
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


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


def _safe_published_at(value):
    if not value:
        return None
    if hasattr(value, "tzinfo"):
        return value
    text = str(value).strip()
    parsed = parse_datetime(text)
    if parsed is None:
        date_value = parse_date(text[:10])
        if date_value:
            parsed = datetime.combine(date_value, time.min).replace(tzinfo=timezone.get_current_timezone())
    if parsed is not None and timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _safe_decimal(value):
    if value in (None, ""):
        return None
    try:
        cleaned = re.sub(r"[^0-9.\-]", "", str(value).replace(",", ""))
        return Decimal(cleaned) if cleaned and cleaned not in {".", "-", "-."} else None
    except (InvalidOperation, ValueError):
        return None


def _safe_job_url(value):
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return ""
    hostname = parsed.hostname.lower().rstrip(".")
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith((".localhost", ".local")):
        return ""
    try:
        literal_ip = ipaddress.ip_address(hostname)
        if not literal_ip.is_global:
            return ""
    except ValueError:
        pass
    return raw


def _upsert_job(source, item):
    # Normalize common public job-board API field names before persistence.
    item = dict(item)
    aliases = {
        "title": ("jobTitle", "position"),
        "company": ("companyName", "company_name", "employer"),
        "url": ("jobUrl", "hostedUrl", "applyUrl", "absolute_url", "link"),
        "description": ("jobDescription", "descriptionPlain", "content", "summary"),
        "location": ("jobGeo", "candidate_required_location"),
        "published_at": ("publication_date", "pubDate", "created_at"),
    }
    for canonical, keys in aliases.items():
        if not item.get(canonical):
            item[canonical] = next((item.get(key) for key in keys if item.get(key)), None)
    title = str(item.get("title") or item.get("name") or "").strip()[:255]
    url = _safe_job_url(item.get("url") or item.get("link") or item.get("absolute_url"))
    if not title or not url:
        return None
    description = str(item.get("description") or item.get("summary") or item.get("content") or "")
    if "<" in description and ">" in description:
        try:
            from bs4 import BeautifulSoup
            description = BeautifulSoup(description, "html.parser").get_text(" ", strip=True)
        except Exception:
            description = re.sub(r"<[^>]+>", " ", description)
    description = description[:30000]
    loc = item.get("location")
    if isinstance(loc, dict):
        loc = loc.get("name", "")
    canonical_key = _canonical_key({**item, "url": url, "title": title})
    raw_external_id = item.get("id") or item.get("guid") or item.get("external_id") or item.get("jobId")
    external_id = str(raw_external_id or __import__("hashlib").sha256(canonical_key.encode("utf-8")).hexdigest())[:255]
    existing = JobOpportunity.objects.filter(
        user=source.user, canonical_key=canonical_key).first() if canonical_key else None
    defaults = {
        "title": title, "company": str(item.get("company") or item.get("employer") or item.get("company_name") or source.name)[:255],
        "description": description, "url": url[:500],
        "location": str(loc or "")[:255], "is_remote": bool(item.get("remote") or item.get("is_remote") or "remote" in str(loc or "").lower()),
        "published_at": _safe_published_at(item.get("published_at") or item.get("date") or item.get("first_published") or item.get("updated_at")),
        "salary_min": _safe_decimal(item.get("salary_min") or item.get("min_salary")), "salary_max": _safe_decimal(item.get("salary_max") or item.get("max_salary")),
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
    JobParserService.analyze(
        job, user=source.user,
        use_ai=bool((source.config or {}).get("ai_analyze_on_import", False)),
    )
    JobMatchingService.calculate(source.user, job)
    return job


def _rss_items(content):
    """Parse RSS 2.0 and Atom feeds without relying on Element truthiness.

    RSS elements often have no children, so ``element_a or element_b`` is not
    a safe way to select XML nodes. Atom links also commonly store their URL in
    an ``href`` attribute instead of element text.
    """
    try:
        root = ET.fromstring(content)
    except (ET.ParseError, TypeError):
        # Some public feeds contain illegal XML control characters. Retry only
        # after decoding bytes safely; strings are supported as well.
        raw = content.decode("utf-8", errors="replace") if isinstance(content, bytes) else str(content)
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", raw)
        try:
            root = ET.fromstring(cleaned)
        except ET.ParseError as exc:
            raise ValueError(f"RSS/Atom feed is not valid XML: {exc}") from exc

    atom_ns = "{http://www.w3.org/2005/Atom}"
    entries = root.findall(".//item") + root.findall(f".//{atom_ns}entry")

    def child_text(node, *names):
        wanted = set(names)
        for child in list(node):
            local_name = child.tag.rsplit("}", 1)[-1] if isinstance(child.tag, str) else ""
            if local_name in wanted:
                value = "".join(child.itertext()).strip()
                if value:
                    return value
        return ""

    items = []
    for node in entries:
        link = ""
        for child in list(node):
            local_name = child.tag.rsplit("}", 1)[-1] if isinstance(child.tag, str) else ""
            if local_name != "link":
                continue
            href = (child.attrib.get("href") or "").strip()
            rel = (child.attrib.get("rel") or "alternate").strip().lower()
            value = href or (child.text or "").strip()
            if value and (rel == "alternate" or not link):
                link = value
                if rel == "alternate":
                    break

        link = link or child_text(node, "link")
        identifier = child_text(node, "guid", "id") or link
        items.append({
            "id": identifier,
            "title": child_text(node, "title"),
            "description": child_text(node, "description", "summary", "content"),
            "company": child_text(node, "company", "employer"),
            "location": child_text(node, "location"),
            "url": link,
        })
    return items


@shared_task(bind=True, autoretry_for=(requests.RequestException, TimeoutError, socket.gaierror), retry_backoff=True, max_retries=3)
def sync_job_source(self, source_id):
    source = JobSource.objects.get(pk=source_id)
    if not source.enabled:
        return {"source_id": source.id, "status": "skipped", "reason": "source_disabled"}
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
            from scraper.services import fetch_public
            content, content_type, final_url, status_code = fetch_public(url, timeout=20)
            fetch_meta = {"status_code": status_code, "content_type": content_type, "bytes": len(content), "url": final_url}
            if source.source_type == JobSource.SourceType.RSS or "rss" in content_type or "atom" in content_type or "xml" in content_type:
                items = _rss_items(content)
            else:
                try:
                    data = json.loads(content.decode("utf-8", errors="replace"))
                except (ValueError, TypeError):
                    items = _rss_items(content)
                    data = None
                if data is not None:
                    adapter = (source.config or {}).get("adapter")
                    if adapter == "greenhouse":
                        items = [{**x, "company": x.get("company_name") or source.name, "location": (x.get("location") or {}).get("name", ""), "url": x.get("absolute_url"), "description": x.get("content", ""), "published_at": x.get("first_published")} for x in (data.get("jobs", []) if isinstance(data, dict) else [])]
                    elif adapter == "lever":
                        items = [{**x, "url": x.get("hostedUrl") or x.get("applyUrl"), "description": x.get("descriptionPlain") or x.get("description", ""), "company": source.name, "location": (x.get("categories") or {}).get("location", "")} for x in (data if isinstance(data, list) else [])]
                    elif adapter == "remotive":
                        items = [{**x, "location": x.get("candidate_required_location") or "Remote", "published_at": x.get("publication_date"), "remote": True} for x in (data.get("jobs", []) if isinstance(data, dict) else [])]
                    elif adapter == "arbeitnow":
                        items = [{**x, "published_at": x.get("created_at"), "remote": bool(x.get("remote"))} for x in (data.get("data", []) if isinstance(data, dict) else [])]
                    elif adapter == "jobicy":
                        items = [{**x, "title": x.get("jobTitle"), "company": x.get("companyName"), "url": x.get("jobUrl"), "description": x.get("jobDescription"), "location": x.get("jobGeo"), "published_at": x.get("pubDate"), "remote": True} for x in (data.get("jobs", []) if isinstance(data, dict) else [])]
                    elif isinstance(data, dict):
                        configured_items = _json_path(data, (source.config or {}).get("items_path", ""))
                        if configured_items is not None and (source.config or {}).get("items_path"):
                            items = configured_items
                        else:
                            items = data.get("items") or data.get("jobs") or data.get("results") or data.get("data") or []
                    else:
                        items = data if isinstance(data, list) else []
                    if isinstance(items, dict):
                        items = items.get("items") or items.get("jobs") or items.get("results") or [items]
                    if not isinstance(items, list):
                        items = []
        created = []
        skipped_invalid = 0
        with transaction.atomic():
            for item in items[: max(1, min(source.max_items_per_sync, 500))]:
                if isinstance(item, dict):
                    job = _upsert_job(source, item)
                    if job is None:
                        skipped_invalid += 1
                    else:
                        created.append(job.id)
        source.last_synced_at = timezone.now()
        source.last_sync_status = "completed"
        source.last_sync_error = ""
        source.last_sync_count = len(created)
        source.save(update_fields=["last_synced_at", "last_sync_status",
                    "last_sync_error", "last_sync_count", "updated_at"])
        return {"source_id": source.id, "status": "completed", "jobs": len(created), "skipped_invalid": skipped_invalid, "metadata": fetch_meta}
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
