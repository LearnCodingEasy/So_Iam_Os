from django.db.models import Count
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Website, ParentSelector, ScrapingConfig, ScrapingJob, ScrapedData
from .serializers import WebsiteSerializer, ParentSelectorSerializer, ScrapingConfigSerializer, ScrapingJobSerializer, ScrapedDataSerializer
from .services import ScrapingService


class OwnedQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        if self.action in ("list", "retrieve"):
            return qs.filter(website__created_by=user) if hasattr(self, "nested_website_filter") else qs.filter(created_by=user)
        return qs.filter(website__created_by=user) if hasattr(self, "nested_website_filter") else qs.filter(created_by=user)


class WebsiteViewSet(viewsets.ModelViewSet):
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Website.objects.all().annotate(run_count=Count("scrapingjob"))
        if self.request.user.is_staff:
            return qs
        return qs.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.created_by_id != self.request.user.id and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot edit this source.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by_id != self.request.user.id and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot delete this source.")
        if instance.scrapingjob_set.exists():
            instance.is_active = False
            instance.save(update_fields=["is_active", "updated_at"])
        else:
            instance.delete()

    @action(detail=True, methods=["post"])
    def test_connection(self, request, pk=None):
        website = self.get_object()
        try:
            result = ScrapingService.test_connection(website)
            return Response(result)
        except Exception as exc:
            return Response({"ok": False, "error": str(exc)[:1000]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        website = self.get_object()
        if not website.is_active:
            return Response({"detail": "Source is disabled."}, status=status.HTTP_400_BAD_REQUEST)
        running = website.scrapingjob_set.filter(status="running").exists()
        if running:
            return Response({"detail": "A run is already in progress for this source."}, status=status.HTTP_409_CONFLICT)
        job = ScrapingJob.objects.create(website=website, target_url=website.base_url, status="pending", trigger_type="manual")
        try:
            from .tasks import run_scraping_job
            task = run_scraping_job.delay(str(job.pk))
            return Response({"job": ScrapingJobSerializer(job).data, "task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        except Exception as exc:
            job.status = "failed"
            job.error_message = "Background queue unavailable. Configure Celery/Redis before running scraper tasks."
            job.completed_at = timezone.now()
            job.save(update_fields=["status", "error_message", "completed_at"])
            return Response({"detail": job.error_message, "job": ScrapingJobSerializer(job).data}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        sources = self.get_queryset()
        jobs = ScrapingJob.objects.filter(website__in=sources)
        return Response({
            "sources_total": sources.count(),
            "sources_active": sources.filter(is_active=True).count(),
            "runs_total": jobs.count(),
            "runs_failed": jobs.filter(status="failed").count(),
            "runs_completed": jobs.filter(status="completed").count(),
            "items_scraped": sum(j.items_scraped for j in jobs.only("items_scraped")),
            "last_run_at": jobs.order_by("-started_at").values_list("started_at", flat=True).first(),
        })


class ParentSelectorViewSet(viewsets.ModelViewSet):
    serializer_class = ParentSelectorSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        website = serializer.validated_data["website"]
        if not self.request.user.is_staff and website.created_by_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot attach selectors to this source.")
        serializer.save()

    def perform_update(self, serializer):
        website = serializer.validated_data.get("website", serializer.instance.website)
        if not self.request.user.is_staff and website.created_by_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot attach selectors to this source.")
        serializer.save()

    def get_queryset(self):
        qs = ParentSelector.objects.select_related("website")
        if self.request.user.is_staff: return qs
        return qs.filter(website__created_by=self.request.user)


class ScrapingConfigViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapingConfigSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        parent = serializer.validated_data["parent"]
        if not self.request.user.is_staff and parent.website.created_by_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot configure this source.")
        serializer.save()

    def perform_update(self, serializer):
        parent = serializer.validated_data.get("parent", serializer.instance.parent)
        if not self.request.user.is_staff and parent.website.created_by_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot configure this source.")
        serializer.save()

    def get_queryset(self):
        qs = ScrapingConfig.objects.select_related("parent__website")
        if self.request.user.is_staff: return qs
        return qs.filter(parent__website__created_by=self.request.user)


class ScrapingJobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScrapingJobSerializer
    permission_classes = [IsAuthenticated]
    queryset = ScrapingJob.objects.select_related("website").all()
    def get_queryset(self):
        qs = super().get_queryset()
        return qs if self.request.user.is_staff else qs.filter(website__created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def results(self, request, pk=None):
        job = self.get_object()
        data = ScrapedData.objects.filter(job=job).order_by("-scraped_at")[:500]
        return Response(ScrapedDataSerializer(data, many=True).data)
