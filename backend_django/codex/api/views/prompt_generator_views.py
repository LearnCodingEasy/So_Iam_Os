from codex.services.extensions import build_prompt
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class PromptGeneratorView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        prompt = build_prompt(project, request.data.get(
            "prompt_type", "development"), request.data.get("goal", ""), request.data.get("paths") or [])
        return Response({"prompt": prompt, "copy_ready": True})
