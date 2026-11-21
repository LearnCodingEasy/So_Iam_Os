from codex.services.intelligence import build_graph
from codex.models import ArchitectureNode, ArchitectureEdge
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class GraphView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        nodes = list(ArchitectureNode.objects.filter(project=project).values(
            'id', 'key', 'kind', 'label', 'path', 'metadata'))
        edges = list(ArchitectureEdge.objects.filter(project=project).values(
            'source_id', 'target_id', 'relation', 'metadata'))
        return Response({'nodes': nodes, 'edges': edges})

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response(build_graph(project))
