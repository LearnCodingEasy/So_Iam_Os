
import logging
from datetime import timedelta

from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .services import TaskService
from .daily_generation import DailyTaskGenerationService
from core.cache_utils import invalidate_dashboard

logger = logging.getLogger(__name__)


class TaskPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination

    SEARCH_FIELDS = ("title", "description")
    RELATED_FIELDS = (
        "goal",
        "learning_goal",
        "learning_path",
        "learning_topic",
        "skill",
    )

    def has_field(self, name):
        try:
            Task._meta.get_field(name)
            return True
        except FieldDoesNotExist:
            return False

    def invalidate_cache(self):
        invalidate_dashboard(self.request.user.id)

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        related = [
            name for name in self.RELATED_FIELDS
            if self.has_field(name)
        ]
        if related:
            qs = qs.select_related(*related)

        params = self.request.query_params

        # Exact filters
        for param, field in (
            ("status", "status"),
            ("priority", "priority"),
            ("goal_id", "goal_id"),
            ("learning_goal_id", "learning_goal_id"),
            ("learning_path_id", "learning_path_id"),
            ("skill_id", "skill_id"),
        ):
            value = params.get(param)
            if value and self.has_field(field):
                qs = qs.filter(**{field: value})

        # Exact date and date range
        date_value = params.get("date")
        if date_value:
            parsed = parse_date(date_value)
            if parsed and self.has_field("scheduled_date"):
                qs = qs.filter(scheduled_date=parsed)
            elif self.has_field("scheduled_date"):
                qs = qs.none()

        for param, lookup in (
            ("date_from", "scheduled_date__gte"),
            ("date_to", "scheduled_date__lte"),
        ):
            value = params.get(param)
            if value and self.has_field("scheduled_date"):
                parsed = parse_date(value)
                if parsed:
                    qs = qs.filter(**{lookup: parsed})
                else:
                    qs = qs.none()

        # Overdue: not completed and scheduled before today
        if params.get("overdue") == "true":
            if self.has_field("scheduled_date") and self.has_field("status"):
                completed = self.completed_status_values()
                qs = qs.filter(
                    scheduled_date__lt=timezone.localdate()
                ).exclude(status__in=completed)

        # Text search
        search = params.get("search", "").strip()
        if search:
            condition = Q()
            for field in self.SEARCH_FIELDS:
                if self.has_field(field):
                    condition |= Q(**{f"{field}__icontains": search})
            if condition:
                qs = qs.filter(condition)

        # Safe ordering allowlist
        ordering = params.get("ordering", "-id")
        allowed = {
            "id", "-id",
            "scheduled_date", "-scheduled_date",
            "status", "-status",
            "priority", "-priority",
            "created_at", "-created_at",
        }
        ordering_fields = {
            item.lstrip("-") for item in allowed
        }
        if (
            ordering in allowed
            and all(self.has_field(f) for f in ordering_fields
                    if f == ordering.lstrip("-"))
        ):
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-id")

        return qs

    def completed_status_values(self):
        if not self.has_field("status"):
            return ["completed"]

        field = Task._meta.get_field("status")
        choices = dict(field.flatchoices)
        matches = [
            value for value, label in choices.items()
            if str(value).lower() in {"completed", "complete", "done"}
            or str(label).lower() in {"completed", "complete", "done"}
        ]
        return matches or ["completed"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self.invalidate_cache()

    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.invalidate_cache()

    def list(self, request, *args, **kwargs):
        # Invalid status values receive a clear validation response.
        value = request.query_params.get("status")
        if value and self.has_field("status"):
            field = Task._meta.get_field("status")
            valid_values = {str(v) for v, _ in field.flatchoices}
            if valid_values and value not in valid_values:
                return Response(
                    {"status": ["Invalid status value."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        qs = self.get_queryset()
        if not self.has_field("scheduled_date"):
            return Response(
                {"detail": "scheduled_date is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = qs.filter(scheduled_date=timezone.localdate())
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                self.get_serializer(page, many=True).data
            )
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        count = request.data.get("count")
        use_celery = request.data.get("async", True)
        provider = request.data.get("provider")
        model = request.data.get("model")

        if not isinstance(use_celery, bool):
            return Response(
                {"async": ["Must be a boolean."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if count is not None:
            try:
                count = int(count)
            except (TypeError, ValueError):
                return Response(
                    {"count": ["Must be an integer."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if count < 1 or count > 100:
                return Response(
                    {"count": ["Must be between 1 and 100."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if use_celery:
            try:
                from .tasks import generate_daily_learning_tasks

                job = generate_daily_learning_tasks.delay(
                    request.user.id,
                    count=count,
                    provider=provider,
                    model=model,
                )
                return Response(
                    {"status": "queued", "task_id": job.id},
                    status=status.HTTP_202_ACCEPTED,
                )
            except Exception:
                logger.exception(
                    "Failed to queue daily task generation for user %s",
                    request.user.id,
                )

        try:
            created = DailyTaskGenerationService(
                request.user
            ).generate(
                count=count,
                provider=provider,
                model=model,
            )
        except (ValidationError, ValueError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception(
                "Synchronous task generation failed for user %s",
                request.user.id,
            )
            return Response(
                {"detail": "Task generation failed."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        self.invalidate_cache()
        return Response(
            self.get_serializer(created, many=True).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        actual_minutes = request.data.get("actual_minutes")

        if actual_minutes is not None:
            try:
                actual_minutes = int(actual_minutes)
            except (TypeError, ValueError):
                return Response(
                    {"actual_minutes": ["Must be an integer."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if actual_minutes < 0:
                return Response(
                    {"actual_minutes": ["Cannot be negative."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        task = self.get_object()
        try:
            with transaction.atomic():
                task = TaskService.complete(task, actual_minutes)
                transaction.on_commit(self.invalidate_cache)
        except (ValidationError, ValueError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def postpone(self, request, pk=None):
        until = request.data.get("until")
        if not until:
            return Response(
                {"until": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Accept an ISO date or ISO datetime.
        parsed_date = parse_date(until)
        parsed_datetime = parse_datetime(until)
        if not parsed_date and not parsed_datetime:
            return Response(
                {"until": ["Use an ISO date or datetime."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = self.get_object()
        try:
            with transaction.atomic():
                task = TaskService.postpone(task, until)
                transaction.on_commit(self.invalidate_cache)
        except (ValidationError, ValueError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        return self.change_status(request, "in_progress")

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self.change_status(request, "cancelled")

    @action(detail=True, methods=["post"])
    def reopen(self, request, pk=None):
        return self.change_status(request, "pending")

    def change_status(self, request, target):
        task = self.get_object()

        if not self.has_field("status"):
            return Response(
                {"detail": "Task status is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        field = Task._meta.get_field("status")
        choices = dict(field.flatchoices)
        choice_lookup = {
            str(value).lower(): value for value in choices
        }
        choice_lookup.update({
            str(label).lower(): value
            for value, label in choices.items()
        })
        actual_value = choice_lookup.get(target)

        if actual_value is None:
            return Response(
                {
                    "detail": (
                        f"Status '{target}' is not configured "
                        "in the Task model."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prevent reopening or cancelling without a valid transition
        current = str(task.status).lower()
        completed = {str(v).lower() for v in self.completed_status_values()}

        if target == "in_progress" and current in completed:
            return Response(
                {"detail": "Completed tasks cannot be started."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target == "pending" and current not in completed:
            return Response(
                {"detail": "Only completed tasks can be reopened."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = actual_value
        task.save(update_fields=["status"])
        self.invalidate_cache()
        return Response(self.get_serializer(task).data)

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        qs = self.get_queryset()
        if not self.has_field("status"):
            return Response(
                {"detail": "Task status is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rows = qs.values("status").annotate(total=Count("id"))
        by_status = {
            str(row["status"]): row["total"] for row in rows
        }
        total = qs.count()
        completed_count = sum(
            by_status.get(str(value), 0)
            for value in self.completed_status_values()
        )

        return Response({
            "total": total,
            "completed": completed_count,
            "remaining": total - completed_count,
            "completion_percent": (
                round(completed_count * 100 / total, 2)
                if total else 0
            ),
            "by_status": by_status,
        })

    @action(detail=False, methods=["get"], url_path="progress")
    def progress(self, request):
        return self.stats(request)

    @action(detail=False, methods=["get"], url_path="calendar")
    def calendar(self, request):
        if not self.has_field("scheduled_date"):
            return Response(
                {"detail": "scheduled_date is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start = request.query_params.get("date_from")
        end = request.query_params.get("date_to")

        start_date = parse_date(start) if start else timezone.localdate()
        end_date = parse_date(end) if end else (
            start_date + timedelta(days=30)
        )

        if not start_date or not end_date or start_date > end_date:
            return Response(
                {"detail": "Invalid date range."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (end_date - start_date).days > 366:
            return Response(
                {"detail": "Calendar range cannot exceed 366 days."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = self.get_queryset().filter(
            scheduled_date__range=(start_date, end_date)
        )
        rows = qs.values("scheduled_date").annotate(
            total=Count("id")
        ).order_by("scheduled_date")

        return Response([
            {
                "date": row["scheduled_date"],
                "total": row["total"],
            }
            for row in rows
        ])

    @action(detail=False, methods=["get"], url_path="overdue")
    def overdue(self, request):
        if not self.has_field("scheduled_date"):
            return Response(
                {"detail": "scheduled_date is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = self.get_queryset().filter(
            scheduled_date__lt=timezone.localdate()
        )
        if self.has_field("status"):
            qs = qs.exclude(
                status__in=self.completed_status_values()
            )

        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                self.get_serializer(page, many=True).data
            )
        return Response(self.get_serializer(qs, many=True).data)

    @action(
        detail=False,
        methods=["get"],
        url_path="generation-status/(?P<task_id>[^/.]+)",
    )
    def generation_status(self, request, task_id=None):
        # Security requirement: the Celery task must publish its owner ID
        # in result metadata. Never expose arbitrary Celery task results.
        try:
            from celery.result import AsyncResult
            from .tasks import generate_daily_learning_tasks

            result = AsyncResult(
                task_id,
                app=generate_daily_learning_tasks.app,
            )
            info = result.info
            owner_id = (
                info.get("user_id")
                if isinstance(info, dict)
                else None
            )

            if str(owner_id) != str(request.user.id):
                return Response(
                    {"detail": "Generation job not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            payload = {
                "task_id": task_id,
                "status": result.status.lower(),
            }
            if result.successful():
                payload["result"] = result.result
            elif result.failed():
                payload["detail"] = "Generation failed."

            return Response(payload)
        except Exception:
            logger.exception(
                "Unable to inspect generation job %s", task_id
            )
            return Response(
                {"detail": "Unable to retrieve generation status."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
