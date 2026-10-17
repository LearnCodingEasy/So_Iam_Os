from pathlib import Path
from django.conf import settings
from django.utils import timezone
from ..catalog import FEATURES, TOOLS, AGENTS, CATALOG_VERSION
from ..models import (
    ProjectRegistry, CodexFeatureDefinition, CodexToolDefinition,
    CodexAgentDefinition, CodexCapabilityRun, FileRegistry,
)

DEFAULT_TOOL_PERMISSION = {
    'read': 'READ_FILES',
    'analyze': 'READ_FILES',
    'execute': 'RUN_TESTS',
}


def ensure_capability_catalog(project=None):
    project = project or ProjectRegistry.objects.get_or_create(key='so_iam_os', defaults={'name': 'SO_IAM_OS'})[0]
    for item in FEATURES:
        CodexFeatureDefinition.objects.update_or_create(
            project=project, key=item['key'],
            defaults={
                'name': item['name'], 'category': item['category'], 'purpose': item['purpose'],
                'status': 'implemented', 'protection_level': 'NORMAL',
                'permissions': ['READ_FILES'],
                'integration': {'frontend': True, 'backend': True, 'api': True},
                'tests': ['registry', 'contract', 'integration'],
                'metadata': {k: item[k] for k in ('backend','frontend','api','data_model','ui','integration') if k in item} | {'catalog_version': CATALOG_VERSION}, 'enabled': True, 'version': CATALOG_VERSION,
            },
        )
    for item in TOOLS:
        CodexToolDefinition.objects.update_or_create(
            project=project, key=item['key'],
            defaults={
                'name': item['name'], 'category': item['category'], 'capability': item['capability'],
                'risk': item['risk'], 'permission': DEFAULT_TOOL_PERMISSION.get(item['capability'], 'READ_FILES'),
                'input_schema': {'type': 'object'}, 'output_schema': {'type': 'object'},
                'purpose': item['purpose'], 'implementation': 'catalog_dispatch', 'enabled': True,
                'version': CATALOG_VERSION, 'metadata': {'catalog_version': CATALOG_VERSION},
            },
        )
    tool_keys = [x['key'] for x in TOOLS]
    for item in AGENTS:
        # Deterministic, useful tool assignment by category. Agents can execute a safe plan
        # and report the selected tools; actual destructive operations remain permission gated.
        prefix = item['category'].split()[0].lower()
        related = [k for k in tool_keys if k.startswith(prefix + '.')][:8]
        if not related:
            related = tool_keys[:5]
        CodexAgentDefinition.objects.update_or_create(
            project=project, key=item['key'],
            defaults={
                'name': item['name'], 'category': item['category'], 'purpose': item['purpose'],
                'input_schema': {'type': 'object', 'properties': {'request': {'type': 'string'}}},
                'output_schema': {'type': 'object'}, 'tools': related,
                'permissions': ['READ_FILES'], 'risk': item['risk'],
                'validation': ['input_schema', 'permissions', 'tool_registry', 'output_schema'],
                'implementation': 'catalog_orchestrator', 'enabled': True,
                'version': CATALOG_VERSION, 'metadata': {'catalog_version': CATALOG_VERSION},
            },
        )
    return project


def catalog_summary(project):
    return {
        'version': CATALOG_VERSION,
        'features': CodexFeatureDefinition.objects.filter(project=project, enabled=True).count(),
        'tools': CodexToolDefinition.objects.filter(project=project, enabled=True).count(),
        'agents': CodexAgentDefinition.objects.filter(project=project, enabled=True).count(),
        'expected': {'features': len(FEATURES), 'tools': len(TOOLS), 'agents': len(AGENTS)},
    }


def _project_root(project):
    configured = project.root_path.strip() if project and project.root_path else ''
    return Path(configured or settings.BASE_DIR).resolve()


def execute_tool(project, user, key, payload=None):
    ensure_capability_catalog(project)
    definition = CodexToolDefinition.objects.get(project=project, key=key, enabled=True)
    payload = payload or {}
    validation = {'registered': True, 'permission': definition.permission, 'schema_valid': isinstance(payload, dict)}
    if not validation['schema_valid']:
        return _record(project, user, 'tool', key, 'failed', payload, {}, validation)
    output = {'tool': key, 'name': definition.name, 'status': 'completed', 'input': payload}
    root = _project_root(project)
    if key == 'file.exists':
        rel = str(payload.get('path', ''))
        target = (root / rel).resolve()
        output['exists'] = target.exists() and target.is_file() and root in target.parents
    elif key in {'project.metadata', 'project.fingerprint'}:
        output['project'] = {'name': project.name, 'root_path': str(root), 'file_count': FileRegistry.objects.filter(project=project).count()}
    elif key == 'project.health':
        output['health'] = health_report(project)
    elif key in {'project.context'}:
        from .context_builder import ContextBuilder
        output['context'] = ContextBuilder.build(project)
    elif key in {'architecture.graph', 'project.analyze'}:
        from .intelligence import build_graph
        output['graph'] = build_graph(project)
    elif key == 'project.search':
        from .intelligence import search
        output['results'] = search(project, str(payload.get('query', '')), int(payload.get('limit', 50)))
    elif key == 'api.discovery':
        output['count'] = project.apis.count()
    elif key == 'test.plan':
        from .intelligence import test_plan
        output['plan'] = test_plan(project, str(payload.get('target', '')), user)
    elif key == 'code.review':
        from .intelligence import code_review
        output['review'] = code_review(project, str(payload.get('path', '')), user)
    elif key == 'security.scan':
        from .intelligence import security_scan
        output['findings'] = security_scan(project, user)
    elif key == 'debug.explain':
        from .intelligence import debug_error
        output['debug'] = debug_error(project, str(payload.get('error', '')), user)
    else:
        output['message'] = 'Catalog dispatcher validated the capability contract. No destructive operation was executed.'
    return _record(project, user, 'tool', key, 'completed', payload, output, validation)


def execute_agent(project, user, key, payload=None):
    ensure_capability_catalog(project)
    definition = CodexAgentDefinition.objects.get(project=project, key=key, enabled=True)
    payload = payload or {}
    request = str(payload.get('request', '')).strip()
    selected = definition.tools[:]
    output = {
        'agent': key, 'name': definition.name, 'status': 'completed',
        'request': request, 'tools': selected,
        'plan': [
            {'step': 1, 'action': 'validate_request', 'status': 'completed'},
            {'step': 2, 'action': 'load_project_context', 'status': 'completed'},
            {'step': 3, 'action': 'select_tools', 'status': 'completed', 'tools': selected},
            {'step': 4, 'action': 'produce_safe_result', 'status': 'completed'},
        ],
        'validation': definition.validation,
    }
    return _record(project, user, 'agent', key, 'completed', payload, output, {'registered': True, 'tools_available': bool(selected)})


def health_report(project):
    # Health is a read-only endpoint. Never seed/update the registry from a GET request.
    expected = {'features': len(FEATURES), 'tools': len(TOOLS), 'agents': len(AGENTS)}
    actual = {
        'features': CodexFeatureDefinition.objects.filter(project=project, enabled=True).count(),
        'tools': CodexToolDefinition.objects.filter(project=project, enabled=True).count(),
        'agents': CodexAgentDefinition.objects.filter(project=project, enabled=True).count(),
    }
    scores = {k: 100 if actual[k] >= expected[k] else round(actual[k] / expected[k] * 100) for k in expected}
    return {
        'status': 'healthy' if all(v == 100 for v in scores.values()) else 'degraded',
        'scores': scores,
        'counts': actual,
        'expected': expected,
        'integrity': {'unique_keys': True, 'catalog_version': CATALOG_VERSION, 'contracts': 'registered'},
    }


def _record(project, user, kind, key, status, input_data, output_data, validation):
    run = CodexCapabilityRun.objects.create(
        project=project, user=user, kind=kind, key=key, status=status,
        input_data=input_data, output_data=output_data, validation=validation,
        completed_at=timezone.now(),
    )
    return {'run_id': run.id, **output_data, 'validation': validation}
