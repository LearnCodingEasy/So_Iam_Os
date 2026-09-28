from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from core.cache_utils import invalidate_dashboard
from .serializers import TaskSerializer
from .services import TaskService
from .daily_generation import DailyTaskGenerationService


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user).select_related(
            "goal", "learning_goal", "learning_path", "learning_topic", "skill"
        )
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        date_filter = self.request.query_params.get("date")
        if date_filter:
            qs = qs.filter(scheduled_date=date_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        tasks = self.get_queryset().filter(scheduled_date=timezone.localdate())
        return Response(self.get_serializer(tasks, many=True).data)

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        count = request.data.get("count")
        use_celery = request.data.get("async", True)
        if use_celery:
            try:
                from .tasks import generate_daily_learning_tasks
                job = generate_daily_learning_tasks.delay(request.user.id, count=count, provider=request.data.get("provider"), model=request.data.get("model"))
                return Response({"status": "queued", "task_id": job.id}, status=202)
            except Exception:
                pass
        created = DailyTaskGenerationService(request.user).generate(count=count, provider=request.data.get("provider"), model=request.data.get("model"))
        return Response(self.get_serializer(created, many=True).data, status=201)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        invalidate_dashboard(request.user.id)
        task = TaskService.complete(
            self.get_object(), request.data.get("actual_minutes"))
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def postpone(self, request, pk=None):
        until = request.data.get("until")
        if not until:
            return Response({"detail": "until is required."}, status=status.HTTP_400_BAD_REQUEST)
        invalidate_dashboard(request.user.id)
        task = TaskService.postpone(self.get_object(), until)
        return Response(self.get_serializer(task).data)
