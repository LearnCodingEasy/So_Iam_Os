"""Safe, pluggable source fetching and persistence for Scraper."""
import ipaddress
import json
import logging
import socket
import hashlib
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from django.db import transaction
from django.utils import timezone

from .models import ScrapingJob, ScrapedData, ScrapingConfig

logger = logging.getLogger(__name__)
USER_AGENT = "SO_IAM_OS-Scraper/1.0 (+public-source-fetcher)"


def validate_public_url(url):
    """Reject non-http(s), credentials, local hostnames and private/reserved IPs."""
    parsed = urlparse(url or "")
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Source URL must use http or https.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in source URLs are not allowed.")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError("Local hostnames are not allowed.")
    try:
        addresses = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            addresses = {ipaddress.ip_address(item[4][0]) for item in socket.getaddrinfo(
                host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)}
        except socket.gaierror as exc:
            raise ValueError("Source hostname could not be resolved.") from exc
    if not addresses or any(not addr.is_global for addr in addresses):
        raise ValueError(
            "Private, loopback, link-local and reserved addresses are not allowed.")
    if parsed.port and parsed.port not in (80, 443):
        raise ValueError("Only standard HTTP/HTTPS ports are allowed.")
    return url


def fetch_public(url, timeout=15):
    validate_public_url(url)
    response = requests.get(
        url, timeout=max(3, min(int(timeout or 15), 30)),
        headers={"User-Agent": USER_AGENT,
                 "Accept": "application/json, application/rss+xml, application/atom+xml, text/html;q=0.9, */*;q=0.5"},
        allow_redirects=False, stream=True,
    )
    try:
        if 300 <= response.status_code < 400:
            raise ValueError(
                "Redirects are disabled for safety. Configure the source with its final public URL.")
        response.raise_for_status()
        length = response.headers.get("Content-Length")
        if length and int(length) > 5 * 1024 * 1024:
            raise ValueError("Source response exceeds the 5 MB limit.")
        chunks, size = [], 0
        for chunk in response.iter_content(65536):
            size += len(chunk)
            if size > 5 * 1024 * 1024:
                raise ValueError("Source response exceeds the 5 MB limit.")
            chunks.append(chunk)
        content = b"".join(chunks)
        content_type = response.headers.get("Content-Type", "").lower()
        final_url = response.url
        status_code = response.status_code
        return content, content_type, final_url, status_code
    finally:
        response.close()


def _text(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def _json_path(data, path):
    if not path:
        return data
    current = data
    for key in path.split("."):
        if isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return None
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def parse_source(website, content, content_type=""):
    """Return normalized generic items. JSON sources may specify config.items_path."""
    kind = website.source_type
    text = content.decode("utf-8", errors="replace")
    if kind == "json" or "json" in content_type or text.lstrip().startswith(("{", "[")):
        payload = json.loads(text)
        items = _json_path(
            payload, (website.config or {}).get("items_path", ""))
        if isinstance(items, dict):
            items = items.get("items", items.get(
                "jobs", items.get("results", items.get("data", [items]))))
        if not isinstance(items, list):
            items = [items] if isinstance(items, dict) else []
        return [dict(item) for item in items if isinstance(item, dict)]
    if kind == "rss" or "xml" in content_type or text.lstrip().startswith("<?xml"):
        root = ET.fromstring(content)
        entries = []
        for node in root.iter():
            if node.tag.rsplit("}", 1)[-1].lower() not in ("item", "entry"):
                continue
            row = {}
            for child in node:
                key = child.tag.rsplit("}", 1)[-1].lower()
                row[key] = child.attrib.get(
                    "href", "") if key == "link" and child.attrib else "".join(child.itertext()).strip()
            if row:
                entries.append(row)
        return entries
    soup = BeautifulSoup(text, "html.parser")
    selector = (website.config or {}).get("item_selector", "")
    rows = []
    if selector:
        for element in soup.select(selector)[:500]:
            row = {}
            fields = (website.config or {}).get("fields", {})
            for name, rule in fields.items():
                if isinstance(rule, str):
                    rule = {"selector": rule}
                child = element.select_one(rule.get("selector", ""))
                if child:
                    value = child.get(rule["attribute"]) if rule.get(
                        "attribute") else child.get_text(" ", strip=True)
                    row[name] = urljoin(website.base_url, value) if rule.get(
                        "attribute") == "href" and value else value
            if not row:
                anchor = element.find("a")
                row = {"title": element.get_text(" ", strip=True), "url": urljoin(
                    website.base_url, anchor.get("href", "")) if anchor else ""}
            rows.append(row)
        return rows

    # Backward-compatible path for the existing ParentSelector/ScrapingConfig models.
    try:
        parent_selectors = website.parent_selectors.prefetch_related(
            "child_fields").all()
    except Exception:
        parent_selectors = []
    for parent in parent_selectors:
        if parent.selector_type != "css":
            continue
        for element in soup.select(parent.selector)[:500]:
            row = {}
            for field in parent.child_fields.all():
                if field.selector_type != "css":
                    continue
                child = element.select_one(field.selector)
                if not child:
                    if field.is_required:
                        row = {}
                        break
                    continue
                value = child.get(
                    field.extract_attr) if field.extract_attr else child.get_text(" ", strip=True)
                if value is not None:
                    if field.extract_attr in ("href", "src"):
                        value = urljoin(website.base_url, value)
                    row[field.field_name] = value
            if row:
                rows.append(row)
    if not rows:
        raise ValueError(
            "HTML source needs config.item_selector or existing CSS ParentSelector/ScrapingConfig fields.")
    return rows


def normalize_item(item, base_url=""):
    def first(*keys):
        for key in keys:
            val = item.get(key)
            if val not in (None, ""):
                if isinstance(val, dict):
                    val = val.get("name") or val.get("value") or val.get("label") or val
                return _text(val)
        return ""

    url = first("url", "link", "job_url", "apply_url", "applyUrl", "hostedUrl", "absolute_url")
    if url and not url.lower().startswith(("http://", "https://")):
        url = urljoin(base_url, url)
    description = first("description", "summary", "content", "details", "descriptionPlain")
    if description:
        # Remove markup from common job-board HTML fields before persistence/AI analysis.
        description = BeautifulSoup(description, "html.parser").get_text(" ", strip=True)
    return {
        "title": first("title", "name", "position", "job_title")[:255],
        "company": first("company", "company_name", "employer", "organization")[:255],
        "description": description[:30000],
        "url": url[:500],
        "location": first("location", "job_location", "city")[:255],
        "published_at": first("published", "pubdate", "published_at", "first_published", "date", "updated_at"),
        "external_id": first("external_id", "id", "guid"),
        "raw": item,
    }


class ScrapingService:
    @staticmethod
    def test_connection(website):
        content, content_type, final_url, status = fetch_public(
            website.base_url, website.request_timeout)
        items = parse_source(website, content, content_type)
        return {"ok": True, "status_code": status, "content_type": content_type, "bytes": len(content), "items_found": len(items), "final_url": final_url}

    @staticmethod
    def start_scraping_job(job_id, use_playwright=False, show_browser=False):
        job = ScrapingJob.objects.select_related(
            "website", "website__created_by").get(id=job_id)
        website = job.website
        job.status = "running"
        job.save(update_fields=["status"])
        website.last_run_at = timezone.now()
        website.last_status = "running"
        website.last_error = ""
        website.save(update_fields=["last_run_at",
                     "last_status", "last_error", "updated_at"])
        try:
            content, content_type, final_url, status = fetch_public(
                job.target_url, website.request_timeout)
            items = parse_source(website, content, content_type)
            records = []
            for raw in items[:500]:
                normalized = normalize_item(raw, website.base_url)
                records.append(ScrapedData(job=job, data=normalized,
                               source_url=normalized["url"] or job.target_url))
            created_count = updated_count = duplicate_count = 0
            owner = website.created_by
            if owner:
                from jobs_opportunity.models import JobOpportunity, JobSource
                source_type = {"json": "api", "rss": "rss", "html": "scraper"}.get(
                    website.source_type, "scraper")
                raw_config = website.config or {}
                mirrored_config = {
                    "managed_by": "scraper",
                    "website_id": str(website.pk),
                    "items_path": raw_config.get("items_path", ""),
                    "adapter": "rss" if website.source_type == "rss" else "generic",
                    "ai_analyze_on_import": bool(raw_config.get("ai_analyze_on_import", False)),
                    "terms_confirmed": bool(raw_config.get("terms_confirmed", False)),
                }
                if website.source_type == "html":
                    def _job_field_rule(field_name):
                        rule = (raw_config.get("fields") or {}).get(field_name, {})
                        if isinstance(rule, str):
                            rule = {"selector": rule}
                        if not isinstance(rule, dict):
                            rule = {}
                        result = {"selector": rule.get("selector", ""), "selector_type": "css"}
                        if rule.get("attribute"):
                            result["attribute"] = rule["attribute"]
                        if field_name == "url":
                            result["base_url"] = website.base_url
                        return result
                    mirrored_config.update({
                        "robots_required": True,
                        "rate_limit_seconds": 1,
                        "card": {"selector": raw_config.get("item_selector", ""), "selector_type": "css"},
                        "title": _job_field_rule("title"),
                        "company": _job_field_rule("company"),
                        "location": _job_field_rule("location"),
                        "description": _job_field_rule("description"),
                        "url": _job_field_rule("url"),
                    })
                job_source, source_created = JobSource.objects.get_or_create(
                    user=owner, name=website.name,
                    defaults={"source_type": source_type, "base_url": website.base_url,
                              "feed_url": website.base_url if source_type in ("api", "rss") else "",
                              "enabled": website.is_active, "config": mirrored_config},
                )
                # Keep only sources managed by this Scraper website in sync; do not
                # overwrite a separately configured Jobs source with the same name.
                if not source_created and (job_source.config or {}).get("managed_by") == "scraper":
                    job_source.source_type = source_type
                    job_source.base_url = website.base_url
                    job_source.feed_url = website.base_url if source_type in ("api", "rss") else ""
                    job_source.enabled = website.is_active
                    job_source.config = mirrored_config
                    job_source.save(update_fields=["source_type", "base_url", "feed_url", "enabled", "config", "updated_at"])
                with transaction.atomic():
                    if records:
                        ScrapedData.objects.bulk_create(records)
                    for record in records:
                        item = record.data
                        if not item.get("title") or not item.get("url", "").startswith(("http://", "https://")):
                            continue
                        external_id = item.get("external_id") or hashlib.sha256(
                            item["url"].split("#")[0].encode()).hexdigest()
                        defaults = {
                            "title": item["title"], "company": item.get("company", ""),
                            "description": item.get("description", "")[:30000],
                            "url": item["url"], "location": item.get("location", ""),
                            "metadata": {"scraper_website_id": str(website.pk), "raw": item.get("raw", {})},
                            "last_checked_at": timezone.now(), "is_active": True,
                        }
                        existing = JobOpportunity.objects.filter(
                            user=owner, source=job_source, external_id=external_id).first()
                        if existing:
                            if existing.url == defaults["url"] and existing.title == defaults["title"] and existing.description == defaults["description"]:
                                duplicate_count += 1
                            else:
                                for key, value in defaults.items():
                                    setattr(existing, key, value)
                                existing.save()
                                updated_count += 1
                        else:
                            existing = JobOpportunity.objects.create(
                                user=owner, source=job_source, external_id=external_id, **defaults)
                            created_count += 1
                            from jobs_opportunity.services import JobParserService, JobMatchingService
                            JobParserService.analyze(
                                existing, user=owner,
                                use_ai=bool(mirrored_config.get("ai_analyze_on_import", False)),
                            )
                            JobMatchingService.calculate(owner, existing)
                            continue
                        from jobs_opportunity.services import JobParserService, JobMatchingService
                        JobParserService.analyze(
                            existing, user=owner,
                            use_ai=bool(mirrored_config.get("ai_analyze_on_import", False)),
                        )
                        JobMatchingService.calculate(owner, existing)
                    job_source.last_synced_at = timezone.now()
                    job_source.last_sync_status = "success"
                    job_source.last_sync_count = len(records)
                    job_source.last_sync_error = ""
                    job_source.save(update_fields=[
                                    "last_synced_at", "last_sync_status", "last_sync_count", "last_sync_error", "updated_at"])
            else:
                with transaction.atomic():
                    if records:
                        ScrapedData.objects.bulk_create(records)
            job.items_scraped = len(records)
            job.items_created = created_count
            job.items_updated = updated_count
            job.items_duplicate = duplicate_count
            job.status = "completed"
            job.completed_at = timezone.now()
            job.save(update_fields=["items_scraped", "items_created",
                     "items_updated", "items_duplicate", "status", "completed_at"])
            website.last_status = "completed"
            website.last_error = ""
            website.save(update_fields=[
                         "last_status", "last_error", "updated_at"])
            return {"items_scraped": len(records), "status_code": status}
        except Exception as exc:
            logger.exception("Scraper run failed for source %s", website.pk)
            job.status = "failed"
            job.error_message = str(exc)[:4000]
            job.completed_at = timezone.now()
            job.save(update_fields=["status", "error_message", "completed_at"])
            website.last_status = "failed"
            website.last_error = str(exc)[:4000]
            website.save(update_fields=[
                         "last_status", "last_error", "updated_at"])
            raise
