from codex.services.capabilities import ensure_capability_catalog, catalog_summary
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityBootstrapView(CapabilityRegistryMixin, APIView):
    def post(self, request):
        project = self.project(create=True)
        ensure_capability_catalog(project)
        return Response(catalog_summary(project), status=200)
