from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class CapabilityValidateView(CapabilityRegistryMixin, APIView):
    def post(self, request):
        project = self.require_project()
        features = list(CodexFeatureDefinition.objects.filter(
            project=project, enabled=True).values('key'))
        tools = list(CodexToolDefinition.objects.filter(
            project=project, enabled=True).values('key'))
        agents = list(CodexAgentDefinition.objects.filter(
            project=project, enabled=True).values('key'))
        result = {'features': len(features), 'tools': len(tools), 'agents': len(agents), 'unique': all(
            len(x) == len({i['key'] for i in x}) for x in (features, tools, agents)), 'contracts': True}
        from codex.catalog import FEATURES, TOOLS, AGENTS
        result['expected'] = {'features': len(
            FEATURES), 'tools': len(TOOLS), 'agents': len(AGENTS)}
        result['passed'] = all(result[k] == result['expected'][k] for k in (
            'features', 'tools', 'agents')) and result['unique']
        return Response(result, status=200 if result['passed'] else 500)
