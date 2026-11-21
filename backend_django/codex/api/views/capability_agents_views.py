from django.db.models import Q
from codex.models import CodexAgentDefinition
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.models import CodexAgentDefinition
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityAgentsView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project = self.require_project()
        qs = CodexAgentDefinition.objects.filter(project=project, enabled=True)
        category = request.query_params.get('category')
        query = request.query_params.get('q', '').strip()
        if category:
            qs = qs.filter(category=category)
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(
                key__icontains=query) | Q(purpose__icontains=query))
        return Response(list(qs.values()))
