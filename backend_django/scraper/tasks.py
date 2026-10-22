from celery import shared_task
from .services import ScrapingService


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def run_scraping_job(self, job_id):
    try:
        return ScrapingService.start_scraping_job(job_id)
    except Exception as exc:
        # The service records terminal state. Avoid retrying validation/parse errors.
        message = str(exc).lower()
        if any(token in message for token in ("connection", "timed out", "temporarily", "502", "503", "504")) and self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        raise
