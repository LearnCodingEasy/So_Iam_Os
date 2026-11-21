from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.api.serializers import SnapshotSerializer
from codex.services.snapshot_service import SnapshotService


class CreateSnapshotView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        obj = SnapshotService.create(
            user=request.user, label=request.data.get("label", "Codex snapshot"))
        return Response(SnapshotSerializer(obj).data, status=201)
