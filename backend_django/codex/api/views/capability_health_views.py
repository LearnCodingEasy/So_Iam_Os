from codex.services.capabilities import health_report
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityHealthView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project = self.require_project()
        return Response(health_report(project))
