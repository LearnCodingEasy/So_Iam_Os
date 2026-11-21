# scraper services and workflows

## Service/task/signal source


### scraper/tasks.py
L6: def run_scraping_job(self, job_id):

### scraper/services/scraper_services.py
L21: def validate_public_url(url):
L47: def fetch_public(url, timeout=15):
L78: def _text(value):
L86: def _json_path(data, path):
L103: def parse_source(website, content, content_type=""):
L188: def normalize_item(item, base_url=""):
L189: def first(*keys):
L217: class ScrapingService:
L219: def test_connection(website):
L226: def start_scraping_job(job_id, use_playwright=False, show_browser=False):
L262: def _job_field_rule(field_name):

### scraper/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
