from codex.services.extensions import bootstrap_workflow, verify_workflow
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class WorkflowView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        bootstrap_workflow(project)
        return Response(verify_workflow(project))

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        return Response(bootstrap_workflow(project))
