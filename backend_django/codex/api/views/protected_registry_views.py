from codex.services.extensions import freeze_item
from codex.models import ProtectedItem
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry, ProtectedItem


# ---------------------------------------------------------------------------
# Codex governance / workflow / local AI / prompt / navigation extensions
# ---------------------------------------------------------------------------


class ProtectedRegistryView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        rows = list(ProtectedItem.objects.filter(project=project).values())
        return Response(rows)

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            item = freeze_item(project, request.user, request.data)
            return Response({"id": item.id, "key": item.key, "approved": item.approved, "frozen": item.frozen}, status=201)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
