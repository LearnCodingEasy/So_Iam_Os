from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Goal
from core.cache_utils import invalidate_dashboard
from .serializers import GoalSerializer
from .services import GoalService


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Goal.objects.filter(user=self.request.user)
            .prefetch_related("skills", "learning_goals")
            .annotate(
                task_count=Count("tasks", distinct=True),
                completed_task_count=Count(
                    "tasks",
                    filter=Q(tasks__status="completed"),
                    distinct=True,
                ),
            )
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        invalidate_dashboard(request.user.id)
        goal = GoalService.complete(
            self.get_object(), request.data.get("notes", ""))
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        goal = self.get_object()
        goal.status = Goal.Status.PAUSED
        goal.save(update_fields=["status", "updated_at"])
        invalidate_dashboard(request.user.id)
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        goal = self.get_object()
        goal.status = Goal.Status.ACTIVE
        goal.save(update_fields=["status", "updated_at"])
        invalidate_dashboard(request.user.id)
        return Response(self.get_serializer(goal).data)

    @action(detail=True, methods=["post"], url_path="progress")
    def progress(self, request, pk=None):
        if "progress_percent" not in request.data:
            return Response({"detail": "progress_percent is required."}, status=status.HTTP_400_BAD_REQUEST)
        goal = GoalService.update_progress(
            self.get_object(), request.data["progress_percent"])
        return Response(self.get_serializer(goal).data)
