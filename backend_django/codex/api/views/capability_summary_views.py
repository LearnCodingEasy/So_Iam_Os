from codex.services.capabilities import catalog_summary
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilitySummaryView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project = self.require_project()
        return Response(catalog_summary(project))
