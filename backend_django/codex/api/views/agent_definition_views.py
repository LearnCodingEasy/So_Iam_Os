from codex.models import CodexAgentDefinition
from codex.models import CodexAgentDefinition
from codex.api.serializers import AgentDefinitionSerializer
from codex.api.views.base_views import BaseViewSet


class AgentDefinitionViewSet(BaseViewSet):
    queryset = CodexAgentDefinition.objects.all()
    serializer_class = AgentDefinitionSerializer
    filterset_fields = ["project", "category", "risk", "enabled"]
