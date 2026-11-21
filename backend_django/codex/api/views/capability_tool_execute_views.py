from codex.services.capabilities import execute_tool
from codex.models import CodexToolDefinition
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.models import CodexToolDefinition
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityToolExecuteView(CapabilityRegistryMixin, APIView):
    def post(self, request, key):
        try:
            return Response(execute_tool(self.project(create=True), request.user, key, request.data or {}))
        except CodexToolDefinition.DoesNotExist:
            return Response({'detail': 'Unknown or disabled Codex tool.'}, status=404)
