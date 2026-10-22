"""Safe, opt-in HTML job scraping primitives.

The scraper intentionally refuses to bypass robots.txt, authentication, CAPTCHAs,
or anti-bot controls.  Selectors are supplied by the user through JobSource.config.
"""
from __future__ import annotations

import hashlib
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


def check_robots(url: str, user_agent: str = "So-IAM-OS-JobScraper/1.0") -> bool:
    parsed = urllib.parse.urlparse(url)
    robots_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))
    parser = urllib.robotparser.RobotFileParser(robots_url)
    try:
        parser.read()
    except Exception as exc:
        raise ScraperPolicyError(
            f"Could not verify robots.txt for {parsed.netloc}: {exc}") from exc
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
    if not check_robots(url, user_agent=user_agent):
        raise ScraperPolicyError(
            "robots.txt disallows this URL for the configured scraper user-agent.")
    delay = max(0.25, min(float(rate_limit_seconds or 1), 30))
    time.sleep(delay)
    response = requests.get(url, timeout=20, headers={
                            "User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"})
    response.raise_for_status()
    jobs = extract_jobs(response.text, {
                        **mapping, "url": {**(mapping.get("url") or {}), "base_url": url}})
    return jobs, {"status_code": response.status_code, "url": url, "count": len(jobs)}
