from codex.services.extensions import create_local_job
from codex.models import LocalAIJob
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry, LocalAIJob
from codex.api.serializers import LocalAIJobSerializer


class LocalAIJobViewSet(ReadOnlyModelViewSet):
    queryset = LocalAIJob.objects.all()
    serializer_class = LocalAIJobSerializer
    permission_classes = [CodexAuthenticated]
    filterset_fields = ["project", "task_type", "status", "provider"]


class LocalAIJobsView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        qs = LocalAIJob.objects.filter(
            project=project).order_by("-created_at")[:100]
        return Response(list(qs.values()))

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        task_type = str(request.data.get("task_type", "metadata"))
        allowed = {x[0] for x in LocalAIJob.TASK_CHOICES}
        if task_type not in allowed:
            return Response({"detail": "Unsupported local AI task type."}, status=400)
        job = create_local_job(project, request.user,
                               task_type, request.data.get("input_data") or {})
        return Response({"id": job.id, "status": job.status, "provider": job.provider}, status=202)


class LocalAIJobDetailView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request, job_id):
        try:
            job = LocalAIJob.objects.get(id=job_id)
        except LocalAIJob.DoesNotExist:
            return Response({"detail": "Local AI job not found."}, status=404)
        return Response({
            "id": job.id, "status": job.status, "task_type": job.task_type,
            "provider": job.provider, "result": job.result, "error": job.error,
            "created_at": job.created_at, "started_at": job.started_at, "completed_at": job.completed_at,
        })
