from codex.models import CodexToolDefinition
from codex.models import CodexToolDefinition
from codex.api.serializers import ToolDefinitionSerializer
from codex.api.views.base_views import BaseViewSet


class ToolDefinitionViewSet(BaseViewSet):
    queryset = CodexToolDefinition.objects.all()
    serializer_class = ToolDefinitionSerializer
    filterset_fields = ["project", "category", "risk", "enabled"]
