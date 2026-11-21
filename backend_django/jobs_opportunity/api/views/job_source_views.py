import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobSource, JobSourceSyncRun
from jobs_opportunity.api.serializers import JobSourceSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobSourceViewSet(UserOwnedViewSet):
    serializer_class = JobSourceSerializer

    def get_queryset(self): return JobSource.objects.filter(
        user=self.request.user)

    def perform_create(self, serializer): serializer.save(
        user=self.request.user)

    @action(detail=False, methods=["post"], url_path="sync-all")
    def sync_all(self, request):
        """Queue syncs for this user's enabled sources; never scrape globally."""
        sources = self.get_queryset().filter(enabled=True, source_type__in=[JobSource.SourceType.API, JobSource.SourceType.RSS, JobSource.SourceType.SCRAPER]).exclude(base_url="", feed_url="")
        if not sources.exists():
            return Response({"detail": "No enabled API, RSS, or Scraper sources with public URLs are configured.", "queued": 0}, status=status.HTTP_400_BAD_REQUEST)
        from jobs_opportunity.tasks import sync_job_source
        queued = []
        failures = []
        for source in sources:
            sync_run = JobSourceSyncRun.objects.create(
                user=request.user,
                source=source,
                status=JobSourceSyncRun.Status.QUEUED,
            )
            try:
                # Disable Celery publisher retries for HTTP requests. If Redis is
                # down, the endpoint must fail quickly instead of hanging for ~2m.
                task = sync_job_source.apply_async(
                    args=[source.pk, sync_run.pk],
                    retry=False,
                )
                sync_run.celery_task_id = task.id
                sync_run.save(update_fields=["celery_task_id"])
                queued.append({
                    "source_id": source.pk,
                    "source_name": source.name,
                    "sync_run_id": sync_run.pk,
                    "task_id": task.id,
                })
            except Exception as exc:
                sync_run.status = JobSourceSyncRun.Status.FAILED
                sync_run.finished_at = timezone.now()
                sync_run.error_message = "Background queue unavailable."
                sync_run.metadata = {"error_type": exc.__class__.__name__}
                sync_run.save(update_fields=["status", "finished_at", "error_message", "metadata"])
                failures.append({
                    "source_id": source.pk,
                    "source_name": source.name,
                    "sync_run_id": sync_run.pk,
                    "error": "Background queue unavailable",
                })
        response_status = status.HTTP_202_ACCEPTED if queued else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(
            {"queued": len(queued), "sources": queued, "failures": failures},
            status=response_status,
        )

    @action(detail=False, methods=["get"], url_path="sync-runs")
    def sync_runs(self, request):
        runs = JobSourceSyncRun.objects.filter(user=request.user).select_related("source")[:100]
        return Response([
            {
                "id": run.id,
                "source_id": run.source_id,
                "source_name": run.source.name,
                "task_id": run.celery_task_id,
                "status": run.status,
                "started_at": run.started_at,
                "finished_at": run.finished_at,
                "job_count": run.job_count,
                "error": run.error_message,
                "metadata": run.metadata,
                "created_at": run.created_at,
            }
            for run in runs
        ])

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        source = self.get_object()
        if not source.enabled:
            return Response({"detail": "Enable this source after reviewing its URL, configuration, and terms before syncing."}, status=status.HTTP_400_BAD_REQUEST)
        if source.source_type == JobSource.SourceType.MANUAL:
            return Response({"detail": "Manual sources are maintained manually and cannot be synced automatically."}, status=status.HTTP_400_BAD_REQUEST)
        if not (source.feed_url or source.base_url):
            return Response({"detail": "Configure a public source URL before syncing."}, status=status.HTTP_400_BAD_REQUEST)
        from jobs_opportunity.tasks import sync_job_source
        try:
            if request.data.get("background", True) is True:
                sync_run = JobSourceSyncRun.objects.create(
                    user=request.user,
                    source=source,
                    status=JobSourceSyncRun.Status.QUEUED,
                )
                task = sync_job_source.apply_async(
                    args=[source.id, sync_run.id],
                    retry=False,
                )
                sync_run.celery_task_id = task.id
                sync_run.save(update_fields=["celery_task_id"])
                return Response({
                    "queued": True,
                    "task_id": task.id,
                    "sync_run_id": sync_run.id,
                    "source_id": source.id,
                }, status=status.HTTP_202_ACCEPTED)
            return Response(sync_job_source.apply(args=[source.id]).get())
        except Exception:
            return Response({"detail": "Could not queue or execute the source sync. Verify Celery/Redis configuration."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=True, methods=["post"])
    def test(self, request, pk=None):
        source = self.get_object()
        url = source.feed_url or source.base_url
        if source.source_type == JobSource.SourceType.MANUAL:
            return Response({"ok": False, "source_id": source.id, "detail": "Manual sources do not have an automated connection test."}, status=status.HTTP_400_BAD_REQUEST)
        if not url:
            return Response({"ok": False, "source_id": source.id, "detail": "Configure a source URL first."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from jobs_opportunity.tasks import _safe_url, _rss_items, _json_path
            safe_url = _safe_url(url)
            if source.source_type == JobSource.SourceType.SCRAPER:
                if not (source.config or {}).get("terms_confirmed"):
                    return Response({"ok": False, "source_id": source.id, "detail": "Confirm that the source permits scraping before testing it."}, status=status.HTTP_400_BAD_REQUEST)
                from jobs_opportunity.scraper import check_robots, fetch_and_extract
                allowed = check_robots(source.base_url)
                if not allowed:
                    return Response({"ok": False, "robots_allowed": False, "source_id": source.id, "detail": "robots.txt disallows this URL."}, status=status.HTTP_400_BAD_REQUEST)
                items, meta = fetch_and_extract(safe_url, source.config or {}, user_agent="So-IAM-OS-JobScraper/1.0", rate_limit_seconds=0.25)
                return Response({"ok": True, "robots_allowed": True, "source_id": source.id, "items_found": len(items), "meta": meta})

            import json
            response = requests.get(safe_url, timeout=15, allow_redirects=False, headers={
                "User-Agent": "SO_IAM_OS Job Source Test/1.0",
                "Accept": "application/json,application/rss+xml,application/atom+xml,application/xml,text/xml",
            }, stream=True)
            try:
                if 300 <= response.status_code < 400:
                    raise ValueError("Redirects are disabled for safety; configure the final public URL.")
                response.raise_for_status()
                chunks, size = [], 0
                for chunk in response.iter_content(65536):
                    size += len(chunk)
                    if size > 5 * 1024 * 1024:
                        raise ValueError("Source response exceeds the 5 MB limit.")
                    chunks.append(chunk)
                content = b"".join(chunks)
                if source.source_type == JobSource.SourceType.RSS:
                    items = _rss_items(content)
                else:
                    data = json.loads(content.decode("utf-8", errors="replace"))
                    adapter = (source.config or {}).get("adapter")
                    if adapter == "greenhouse": items = data.get("jobs", []) if isinstance(data, dict) else []
                    elif adapter == "remotive": items = data.get("jobs", []) if isinstance(data, dict) else []
                    elif adapter == "arbeitnow": items = data.get("data", []) if isinstance(data, dict) else []
                    elif adapter == "jobicy": items = data.get("jobs", []) if isinstance(data, dict) else []
                    elif adapter == "lever": items = data if isinstance(data, list) else []
                    elif isinstance(data, dict):
                        configured_items = _json_path(data, (source.config or {}).get("items_path", ""))
                        if configured_items is not None and (source.config or {}).get("items_path"):
                            items = configured_items
                        else:
                            items = data.get("items") or data.get("jobs") or data.get("results") or data.get("data") or []
                    else: items = data if isinstance(data, list) else []
                if isinstance(items, dict):
                    items = items.get("items") or items.get("jobs") or items.get("results") or [items]
                return Response({"ok": True, "source_id": source.id, "status_code": response.status_code, "items_found": len(items) if isinstance(items, list) else 0, "bytes": size})
            finally:
                response.close()
        except Exception as exc:
            return Response({"ok": False, "source_id": source.id, "detail": str(exc)[:500]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def preview(self, request, pk=None):
        source = self.get_object()
        if source.source_type != JobSource.SourceType.SCRAPER:
            return Response({"detail": "Preview is only available for HTML scraper sources."}, status=400)
        if not (source.config or {}).get("terms_confirmed"):
            return Response({"detail": "Confirm that this source permits scraping before previewing it."}, status=400)
        from jobs_opportunity.scraper import fetch_and_extract
        items, meta = fetch_and_extract(source.base_url, source.config or {}, user_agent="So-IAM-OS-JobScraper/1.0", rate_limit_seconds=0.25)
        return Response({"items": items[:25], "meta": meta})
