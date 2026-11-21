from codex.services.capabilities import health_report
from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
from codex.services.context_builder import ContextBuilder
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class ProjectContextExportView(CapabilityRegistryMixin, APIView):
    """Export repository context plus an explicitly bounded personal-work context."""

    def get(self, request):
        project = self.require_project()
        context = ContextBuilder.build(project)
        context['codex_capabilities'] = {
            'version': '1.0.0',
            'features': list(CodexFeatureDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'status', 'protection_level', 'permissions')),
            'tools': list(CodexToolDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'capability', 'risk', 'permission', 'input_schema', 'output_schema')),
            'agents': list(CodexAgentDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'purpose', 'tools', 'permissions', 'risk', 'validation')),
        }
        context['health'] = health_report(project)

        # Personal data is always scoped to request.user. Raw knowledge content is opt-in.
        include_personal = request.query_params.get(
            'include_personal', 'true').lower() not in {'0', 'false', 'no'}
        if include_personal:
            from codex.services.user_context import build_user_context
            include_content = request.query_params.get(
                'include_content', 'false').lower() in {'1', 'true', 'yes'}
            context['personal_context'] = build_user_context(
                request.user,
                limit=request.query_params.get('limit', 25),
                include_content=include_content,
            )
        else:
            context['personal_context'] = {
                'scope': 'omitted_by_request',
                'detail': 'Set include_personal=true to include the authenticated user’s Goals, Tasks, Knowledge, and Learning records.',
            }
        return Response(context)
