from codex.models import FileRegistry
from rest_framework.viewsets import ReadOnlyModelViewSet
from codex.permissions import CodexAuthenticated
from codex.models import FileRegistry
from codex.api.serializers import FileSerializer


class FileViewSet(ReadOnlyModelViewSet):
    queryset = FileRegistry.objects.all()
    serializer_class = FileSerializer
    permission_classes = [CodexAuthenticated]
    filterset_fields = ["project", "kind", "app_label", "protected"]
