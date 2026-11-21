from rest_framework.viewsets import ReadOnlyModelViewSet
from codex.permissions import CodexAuthenticated
from codex.models import ProjectSnapshot
from codex.api.serializers import SnapshotSerializer


class SnapshotViewSet(ReadOnlyModelViewSet):
    queryset = ProjectSnapshot.objects.all()
    serializer_class = SnapshotSerializer
    permission_classes = [CodexAuthenticated]
