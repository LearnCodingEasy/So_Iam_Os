from codex.services.intelligence import build_graph
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class BuildWorkspaceView(APIView):
    """Read-only build graph generated from the actual project filesystem."""
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        from codex.services.build_workspace import build_graph, root_for
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"}
        )[0]
        root = root_for(project)
        return Response({"project": project.name, "root_available": root.exists(),
                         "graph": build_graph(project),
                         "semantics": {"file_presence_is_not_execution": True,
                                       "read_only": True}})
