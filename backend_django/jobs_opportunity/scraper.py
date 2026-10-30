"""Safe, opt-in HTML job scraping primitives.

The scraper intentionally refuses to bypass robots.txt, authentication, CAPTCHAs,
or anti-bot controls.  Selectors are supplied by the user through JobSource.config.
"""
from __future__ import annotations

import hashlib
import ipaddress
import socket
import time
import urllib.parse
import urllib.robotparser

import requests


class JobScraperService:
    """
    خدمة سحب وظائف من الإنترنت لتطبيق jobs_opportunity
    """

    def __init__(self, *args, **kwargs):
        # يمكنك إضافة المتغيرات التي تحتاجها هنا عند التهيئة
        pass

    def run(self):
        """
        دالة لتشغيل عملية السحب
        """
        # اكتب الكود الخاص بسحب الوظائف هنا
        print("بدء عملية سحب الوظائف...")
        return True


class ScraperPolicyError(ValueError):
    pass


def _validate_public_url(url: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url or "")
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ScraperPolicyError("Only public HTTP(S) URLs are allowed.")
    if parsed.username or parsed.password:
        raise ScraperPolicyError("Credentials in source URLs are not allowed.")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith((".localhost", ".local")):
        raise ScraperPolicyError("Local hostnames are not allowed.")
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if port not in (80, 443):
            raise ScraperPolicyError("Only standard HTTP/HTTPS ports are allowed.")
        addresses = {ipaddress.ip_address(item[4][0]) for item in socket.getaddrinfo(
            host, port, type=socket.SOCK_STREAM)}
        if not addresses or any(not address.is_global for address in addresses):
            raise ScraperPolicyError("Private, loopback, link-local and reserved addresses are not allowed.")
    except socket.gaierror as exc:
        raise ScraperPolicyError("Source hostname could not be resolved.") from exc
    return parsed


def check_robots(url: str, user_agent: str = "So-IAM-OS-JobScraper/1.0") -> bool:
    parsed = _validate_public_url(url)
    robots_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))
    response = None
    try:
        response = requests.get(robots_url, timeout=10, allow_redirects=False, headers={
            "User-Agent": user_agent, "Accept": "text/plain"
        })
        if 300 <= response.status_code < 400:
            raise ScraperPolicyError("Redirects are disabled while checking robots.txt.")
        if response.status_code == 404:
            lines = []
        else:
            response.raise_for_status()
            if len(response.content) > 512 * 1024:
                raise ScraperPolicyError("robots.txt response exceeds the size limit.")
            lines = response.text.splitlines()
    except ScraperPolicyError:
        raise
    except Exception as exc:
        raise ScraperPolicyError(
            f"Could not verify robots.txt for {parsed.netloc}: {exc.__class__.__name__}") from exc
    finally:
        if response is not None:
            response.close()
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(lines)
    return parser.can_fetch(user_agent, url)


def _load_bs4():
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "BeautifulSoup4 is required for HTML scraping. Install requirements.txt.") from exc
    return BeautifulSoup


def _select(root, selector: str, selector_type: str):
    if not selector:
        return None
    if selector_type == "xpath":
        try:
            from lxml import html  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "lxml is required for XPath selectors. Install requirements.txt.") from exc
        tree = html.fromstring(str(root))
        found = tree.xpath(selector)
        return found[0] if found else None
    return root.select_one(selector)


def _value(element, rule: dict):
    if element is None:
        return ""
    attribute = rule.get("attribute")
    if attribute:
        return str(element.get(attribute, "")).strip()
    return element.get_text(" ", strip=True)


def extract_jobs(html_text: str, mapping: dict) -> list[dict]:
    BeautifulSoup = _load_bs4()
    soup = BeautifulSoup(html_text, "html.parser")
    card_rule = mapping.get("card") or {}
    cards = soup.select(card_rule.get("selector", "body")
                        ) if card_rule.get("selector") else [soup]
    selector_type = card_rule.get("selector_type", "css")
    if selector_type == "xpath":
        try:
            from lxml import html  # type: ignore
            cards = html.fromstring(html_text).xpath(
                card_rule.get("selector", "//body"))
        except ImportError as exc:
            raise RuntimeError(
                "lxml is required for XPath card selectors.") from exc
    jobs = []
    for card in cards:
        item = {}
        for field in ("title", "company", "location", "description", "salary", "url", "published_at", "skills"):
            rule = mapping.get(field) or {}
            element = _select(card, rule.get("selector", ""),
                              rule.get("selector_type", "css"))
            value = _value(element, rule)
            if field == "url" and element is not None and rule.get("attribute", "href"):
                value = urllib.parse.urljoin(rule.get("base_url", ""), value)
            item[field] = value
        if item.get("title") or item.get("url"):
            item["external_id"] = hashlib.sha256(
                (item.get("url") or item.get("title", "")).encode()).hexdigest()[:32]
            jobs.append(item)
    return jobs


def fetch_and_extract(url: str, mapping: dict, *, user_agent: str, rate_limit_seconds: float = 1.0) -> tuple[list[dict], dict]:
    if not mapping.get("terms_confirmed"):
        raise ScraperPolicyError(
            "Scraping is disabled until the user confirms that the source permits it.")
    _validate_public_url(url)
    if not check_robots(url, user_agent=user_agent):
        raise ScraperPolicyError(
            "robots.txt disallows this URL for the configured scraper user-agent.")
    delay = max(0.25, min(float(rate_limit_seconds or 1), 30))
    time.sleep(delay)
    response = requests.get(url, timeout=20, allow_redirects=False, headers={
        "User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"
    }, stream=True)
    try:
        if 300 <= response.status_code < 400:
            raise ScraperPolicyError("Redirects are disabled for source safety; configure the final public URL.")
        response.raise_for_status()
        chunks, size = [], 0
        for chunk in response.iter_content(65536):
            size += len(chunk)
            if size > 5 * 1024 * 1024:
                raise ScraperPolicyError("Source response exceeds the 5 MB limit.")
            chunks.append(chunk)
        content = b"".join(chunks)
        text = content.decode(response.encoding or "utf-8", errors="replace")
        jobs = extract_jobs(text, {
            **mapping, "url": {**(mapping.get("url") or {}), "base_url": url}
        })
        return jobs, {"status_code": response.status_code, "url": response.url, "count": len(jobs), "bytes": size}
    finally:
        response.close()

