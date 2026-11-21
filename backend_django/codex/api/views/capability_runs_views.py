from codex.models import CodexCapabilityRun
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityRunsView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        qs = CodexCapabilityRun.objects.filter(
            project=self.require_project()).order_by('-created_at')[:200]
        return Response(list(qs.values()))
