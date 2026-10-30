"""Development source presets.

These are opt-in presets. Public API documentation is linked in the metadata; users
must configure a specific board/site and confirm the source terms before enabling it.
"""
DEFAULT_JOB_SOURCES = [
    # --- مصادر APIs عامة وموثوقة (تتضمن Python & Web Development) ---
    {"name": "Greenhouse Public Job Board", "source_type": "api",
        "base_url": "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true", "adapter": "greenhouse", "enabled": False},
    {"name": "Lever Postings API", "source_type": "api",
        "base_url": "https://api.lever.co/v0/postings/{site}?mode=json", "adapter": "lever", "enabled": False},
    {"name": "Remotive Public API (Remote Tech & Python)", "source_type": "api",
     "base_url": "https://remotive.com/api/remote-jobs?search=python", "adapter": "remotive", "enabled": True},
    {"name": "Arbeitnow API", "source_type": "api",
        "base_url": "https://www.arbeitnow.com/api/job-board-api", "adapter": "arbeitnow", "enabled": False},
    {"name": "Jobicy Public API (Web & Python)", "source_type": "api",
     "base_url": "https://jobicy.com/api/v2/remote-jobs?tag=python", "adapter": "jobicy", "enabled": False},

    # --- مصادر عبر RSS (ممتازة لجلب وظائف Django وتطوير الويب والمنطقة العربية) ---
    {"name": "Wuzzuf RSS (Egypt & Arab World Web Jobs)", "source_type": "rss",
     "base_url": "https://wuzzuf.net/api/rss/jobs/?filters%5Bq%5D=Python%20Django", "adapter": "rss", "enabled": True},
    {"name": "GitHub Jobs / Python RSS", "source_type": "rss",
        "base_url": "https://jobicy.com/feed/python-jobs", "adapter": "rss", "enabled": False},
    {"name": "Python Org RSS (Official Python Job Board)", "source_type": "rss",
     "base_url": "https://www.python.org/jobs/feed/rss/", "adapter": "rss", "enabled": True},

    # --- مصادر العمل الحر ومنصات التوظيف (Manual / HTML Scraper / APIs) ---
    {"name": "Mostaql Projects (Arabic Freelance - Web & Python)", "source_type": "scraper",
     "base_url": "https://mostaql.com/projects?category=development&sort=latest", "adapter": "html_scraper", "enabled": True},
    {"name": "Khamsat Services / Python (Arabic Micro-tasks)", "source_type": "scraper",
     "base_url": "https://khamsat.com/programming", "adapter": "html_scraper", "enabled": True},
    {"name": "Baibars / Regional Remote Tech Jobs", "source_type": "manual",
        "base_url": "https://www.bayt.com/en/arabic/jobs/python-developer-jobs/", "adapter": "manual", "enabled": False}
]
