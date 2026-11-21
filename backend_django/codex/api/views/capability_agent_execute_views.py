from codex.services.capabilities import execute_agent
from codex.models import CodexAgentDefinition
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.models import CodexAgentDefinition
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityAgentExecuteView(CapabilityRegistryMixin, APIView):
    def post(self, request, key):
        try:
            return Response(execute_agent(self.project(create=True), request.user, key, request.data or {}))
        except CodexAgentDefinition.DoesNotExist:
            return Response({'detail': 'Unknown or disabled Codex agent.'}, status=404)
