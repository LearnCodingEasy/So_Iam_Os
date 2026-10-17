"""Development source presets.

These are opt-in presets. Public API documentation is linked in the metadata; users
must configure a specific board/site and confirm the source terms before enabling it.
"""
DEFAULT_JOB_SOURCES = [
    {"name": "Greenhouse Public Job Board", "source_type": "api", "base_url": "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true", "adapter": "greenhouse", "enabled": False},
    {"name": "Lever Postings API", "source_type": "api", "base_url": "https://api.lever.co/v0/postings/{site}?mode=json", "adapter": "lever", "enabled": False},
    {"name": "Remotive Public API", "source_type": "api", "base_url": "https://remotive.com/api/remote-jobs", "adapter": "remotive", "enabled": False},
    {"name": "Arbeitnow API", "source_type": "api", "base_url": "https://www.arbeitnow.com/api/job-board-api", "adapter": "arbeitnow", "enabled": False},
    {"name": "Jobicy Public API", "source_type": "api", "base_url": "https://jobicy.com/api/v2/remote-jobs", "adapter": "jobicy", "enabled": False},
]
