from rest_framework.viewsets import ReadOnlyModelViewSet
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry
from codex.api.serializers import ProjectSerializer


class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = ProjectRegistry.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [CodexAuthenticated]
