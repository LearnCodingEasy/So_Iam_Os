from codex.services.intelligence import generate_docs
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class DocumentationView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response(generate_docs(project, request.data.get('target', ''), request.user))
