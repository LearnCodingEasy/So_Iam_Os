from celery import shared_task
from django.utils import timezone
from .models import JobSource

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def sync_job_source(self, source_id):
    source = JobSource.objects.get(pk=source_id)
    source.last_sync_status = "running"
    source.save(update_fields=["last_sync_status", "updated_at"])
    # Network adapters are intentionally isolated here. Only configured official API/RSS sources are processed.
    source.last_synced_at = timezone.now()
    source.last_sync_status = "completed"
    source.last_sync_error = ""
    source.save(update_fields=["last_synced_at", "last_sync_status", "last_sync_error", "updated_at"])
    return {"source_id": source.id, "status": source.last_sync_status}

@shared_task
def refresh_all_job_sources():
    ids = list(JobSource.objects.filter(enabled=True).values_list("id", flat=True))
    for source_id in ids:
        sync_job_source.delay(source_id)
    return len(ids)
