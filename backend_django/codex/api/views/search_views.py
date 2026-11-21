from codex.services.intelligence import search as project_search
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class SearchView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'query': request.query_params.get('q', ''), 'results': project_search(project, request.query_params.get('q', ''), int(request.query_params.get('limit', 50)))})
