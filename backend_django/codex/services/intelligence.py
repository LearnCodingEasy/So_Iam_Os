from __future__ import annotations

import ast
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from ..models import (
    APIEndpoint,
    ArchitectureEdge,
    ArchitectureNode,
    CodexFinding,
    CodexPolicy,
    CodexTool,
    FileRegistry,
    ProjectRegistry,
)

EXCLUDED = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'coverage', '.pytest_cache'}
TEXT_EXTENSIONS = {'.py', '.js', '.ts', '.vue', '.json', '.md', '.txt', '.yaml', '.yml', '.scss', '.css', '.html'}
PY_PATTERNS = {
    'subprocess': r'\bsubprocess\.(run|Popen|call|check_call|check_output)\b',
    'shell_true': r'shell\s*=\s*True',
    'eval': r'\beval\s*\(',
    'exec': r'\bexec\s*\(',
    'hardcoded_secret': r'(?i)(api[_-]?key|secret|password|token)\s*=\s*[\'\"][^\'\"]{8,}[\'\"]',
    'dangerous_delete': r'\b(shutil\.rmtree|os\.remove|os\.unlink)\s*\(',
    'raw_sql': r'(?i)\b(SELECT|UPDATE|DELETE|INSERT)\b.{0,80}\+\s*',
}


def _root() -> Path:
    return Path(settings.BASE_DIR).parent


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return ''


def _rel(path: Path) -> str:
    return str(path.relative_to(_root())).replace('\\', '/')


def _file_paths():
    root = _root()
    for path in root.rglob('*'):
        if not path.is_file() or any(p in EXCLUDED for p in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = _rel(path)
        if rel.startswith('.env'):
            continue
        yield path, rel


def ensure_tools(project: ProjectRegistry):
    defaults = [
        ('project.scan', 'Scan the project', 'read', True),
        ('project.search', 'Search project source', 'read', True),
        ('project.graph', 'Build architecture graph', 'read', True),
        ('security.scan', 'Run security heuristics', 'read', True),
        ('code.review', 'Review source safely', 'read', True),
        ('tests.plan', 'Generate a test plan', 'read', True),
        ('agent.plan', 'Create an agent execution plan', 'plan', True),
        ('terminal.safe', 'Run allowlisted development checks', 'execute', False),
        ('automation.plan', 'Create an automation intent without executing it', 'plan', True),
    ]
    for key, name, capability, enabled in defaults:
        CodexTool.objects.update_or_create(project=project, key=key, defaults={
            'name': name, 'capability': capability, 'enabled': enabled,
        })


def ensure_policy(project: ProjectRegistry, user=None):
    policy, _ = CodexPolicy.objects.get_or_create(project=project, user=user, defaults={
        'permissions': {
            'READ_FILES': 'ALLOW', 'SEARCH_PROJECT': 'ALLOW', 'ANALYZE': 'ALLOW',
            'PLAN_CHANGES': 'ALLOW', 'CREATE_SNAPSHOT': 'ALLOW',
            'WRITE_FILES': 'ASK', 'CREATE_FILES': 'ASK', 'DELETE_FILES': 'ASK',
            'RUN_TESTS': 'ASK', 'RUN_COMMANDS': 'ASK', 'DATABASE_OPERATIONS': 'ASK',
            'GIT_OPERATIONS': 'ASK', 'AUTOMATION': 'ASK', 'INSTALL_PACKAGES': 'ASK',
        }
    })
    return policy


def permission(project, user, key: str) -> str:
    return ensure_policy(project, user).permissions.get(key, 'DENY')


def audit(project, user, event_type, action, status='success', payload=None):
    from ..models import CodexAuditEvent
    return CodexAuditEvent.objects.create(project=project, user=user, event_type=event_type,
                                          action=action, status=status, payload=payload or {})


def search(project: ProjectRegistry, query: str, limit=50):
    query = (query or '').strip()
    if not query:
        return []
    q = query.lower()
    results = []
    for path, rel in _file_paths():
        text = _read(path)
        if q in text.lower() or q in rel.lower():
            lines = text.splitlines()
            hits = []
            for idx, line in enumerate(lines, 1):
                if q in line.lower():
                    hits.append({'line': idx, 'text': line.strip()[:500]})
                    if len(hits) >= 8:
                        break
            results.append({'path': rel, 'kind': path.suffix.lower(), 'hits': hits})
            if len(results) >= limit:
                break
    return results


def _python_symbols(text: str):
    symbols = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return symbols
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append({'type': 'class' if isinstance(node, ast.ClassDef) else 'function', 'name': node.name, 'line': node.lineno})
    return symbols


def build_graph(project: ProjectRegistry, refresh=True):
    if refresh:
        ArchitectureNode.objects.filter(project=project).delete()
        ArchitectureEdge.objects.filter(project=project).delete()
    nodes = {}
    def node(key, kind, label, path='', metadata=None):
        obj, _ = ArchitectureNode.objects.get_or_create(project=project, key=key, defaults={
            'kind': kind, 'label': label, 'path': path, 'metadata': metadata or {},
        })
        if obj.kind != kind or obj.label != label or obj.path != path:
            obj.kind, obj.label, obj.path, obj.metadata = kind, label, path, metadata or obj.metadata
            obj.save(update_fields=['kind', 'label', 'path', 'metadata'])
        nodes[key] = obj
        return obj

    for f in FileRegistry.objects.filter(project=project).iterator():
        file_node = node(f'file:{f.path}', 'file', f.path.split('/')[-1], f.path, {'kind': f.kind, 'app': f.app_label})
        if f.app_label:
            app = node(f'app:{f.app_label}', 'app', f.app_label)
            ArchitectureEdge.objects.get_or_create(project=project, source=app, target=file_node, relation='contains')
        if f.kind == 'python':
            text = _read(_root() / f.path)
            for sym in _python_symbols(text):
                s = node(f'symbol:{f.path}:{sym["name"]}:{sym["line"]}', sym['type'], sym['name'], f.path, sym)
                ArchitectureEdge.objects.get_or_create(project=project, source=file_node, target=s, relation='defines')

    for api in APIEndpoint.objects.filter(project=project):
        a = node(f'api:{api.method}:{api.path}:{api.name}', 'api', f'{api.method} {api.path}', metadata={'app': api.app_label, 'source': api.source})
        if api.app_label:
            app = node(f'app:{api.app_label}', 'app', api.app_label)
            ArchitectureEdge.objects.get_or_create(project=project, source=app, target=a, relation='exposes')
    return {'nodes': ArchitectureNode.objects.filter(project=project).count(), 'edges': ArchitectureEdge.objects.filter(project=project).count()}


def impact(project: ProjectRegistry, query: str, limit=100):
    results = search(project, query, limit=limit)
    impacted = []
    for item in results:
        impacted.append({'path': item['path'], 'reason': 'text/reference match', 'hits': item['hits']})
    return {'query': query, 'count': len(impacted), 'items': impacted}


def security_scan(project: ProjectRegistry, user=None):
    CodexFinding.objects.filter(project=project, category='security', resolved=False).delete()
    findings = []
    for path, rel in _file_paths():
        text = _read(path)
        for rule, pattern in PY_PATTERNS.items():
            for m in re.finditer(pattern, text, re.MULTILINE):
                line = text.count('\n', 0, m.start()) + 1
                severity = 'high' if rule in {'shell_true', 'hardcoded_secret', 'dangerous_delete'} else 'medium'
                findings.append(CodexFinding.objects.create(project=project, category='security', severity=severity,
                    title=rule.replace('_', ' ').title(), path=rel, line=line,
                    message=f'Potential {rule.replace("_", " ")} detected. Review before execution/deployment.',
                    metadata={'rule': rule}))
    audit(project, user, 'security_scan', 'security.scan', payload={'findings': len(findings)}) if user else None
    return [{'id': f.id, 'severity': f.severity, 'title': f.title, 'path': f.path, 'line': f.line, 'message': f.message} for f in findings]


def duplicate_scan(project: ProjectRegistry, user=None):
    groups = defaultdict(list)
    for f in FileRegistry.objects.filter(project=project).only('path', 'sha256', 'size'):
        if f.sha256 and f.size > 200:
            groups[(f.sha256, f.size)].append(f.path)
    duplicates = [paths for paths in groups.values() if len(paths) > 1]
    audit(project, user, 'duplicate_scan', 'code.duplicates', payload={'groups': len(duplicates)}) if user else None
    return [{'paths': paths, 'count': len(paths)} for paths in duplicates]


def code_review(project: ProjectRegistry, path: str, user=None):
    target = _root() / path
    text = _read(target)
    findings = []
    if not text:
        return []
    if target.suffix == '.py':
        try:
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and len(node.body) > 80:
                    findings.append({'severity': 'medium', 'title': 'Large function', 'line': node.lineno, 'message': f'{node.name} is large and may benefit from decomposition.'})
        except SyntaxError as exc:
            findings.append({'severity': 'high', 'title': 'Syntax error', 'line': getattr(exc, 'lineno', 1), 'message': str(exc)})
    if 'TODO' in text:
        findings.append({'severity': 'low', 'title': 'TODO markers', 'line': text.find('TODO') and text[:text.find('TODO')].count('\n') + 1, 'message': 'Review TODO markers before release.'})
    audit(project, user, 'code_review', 'code.review', payload={'path': path}) if user else None
    return findings


def test_plan(project: ProjectRegistry, target: str, user=None):
    related = impact(project, target, 40)['items']
    plan = [
        {'type': 'unit', 'action': f'Test core logic related to {target}'},
        {'type': 'api', 'action': f'Test authenticated API contracts related to {target}'},
        {'type': 'integration', 'action': 'Test frontend-to-backend happy path and validation errors'},
        {'type': 'regression', 'action': 'Run existing project test suite and affected-domain tests'},
    ]
    audit(project, user, 'test_plan', 'tests.plan', payload={'target': target, 'related': len(related)}) if user else None
    return {'target': target, 'related': related, 'plan': plan}


def agent_plan(project: ProjectRegistry, request: str, user=None):
    hits = search(project, request, 30)
    actions = [
        {'step': 1, 'tool': 'project.search', 'status': 'ready', 'purpose': 'Understand affected code'},
        {'step': 2, 'tool': 'project.graph', 'status': 'ready', 'purpose': 'Inspect architecture dependencies'},
        {'step': 3, 'tool': 'security.scan', 'status': 'ready', 'purpose': 'Check execution and security impact'},
        {'step': 4, 'tool': 'agent.plan', 'status': 'approval-required', 'purpose': 'Prepare implementation plan'},
        {'step': 5, 'tool': 'terminal.safe', 'status': 'approval-required', 'purpose': 'Run allowlisted checks only'},
    ]
    result = {'request': request, 'mode': 'safe-agent', 'requires_approval': True, 'context_hits': hits,
              'actions': actions, 'guardrails': ['No arbitrary shell', 'No destructive delete', 'No secret access', 'Protected features require approval']}
    audit(project, user, 'agent_plan', 'agent.plan', payload=result) if user else None
    return result

def explain_feature(project: ProjectRegistry, query: str, user=None):
    features = list(project.features.filter(Q(key__icontains=query) | Q(name__icontains=query) | Q(app_label__icontains=query)).values('id','key','name','app_label','description','status','protected')[:20])
    files = project.files.filter(app_label__icontains=query).values('path','kind','app_label','protected')[:120]
    apis = project.apis.filter(Q(app_label__icontains=query) | Q(path__icontains=query)).values('method','path','name','app_label','frontend_service','coverage_status')[:120]
    result = {'query':query,'features':features,'files':list(files),'apis':list(apis),'flow':['Frontend page/component','Store/service','API','Django view/serializer/service','Model/database']}
    audit(project,user,'feature_explain','feature.explain',payload={'query':query}) if user else None
    return result


def debug_error(project: ProjectRegistry, error_text: str, user=None):
    text = error_text or ''
    candidates = []
    for token in re.findall(r'([\w/.-]+\.(?:py|js|ts|vue))(?::(\d+))?', text):
        path, line = token
        if (project.files.filter(path__icontains=path).exists()):
            candidates.append({'path':path,'line':int(line or 0),'reason':'stack trace reference'})
    for word in re.findall(r'\b(?:[A-Z][A-Za-z0-9_]+Error|[A-Z][A-Za-z0-9_]+Exception)\b', text):
        candidates.extend({'path':x['path'],'reason':f'error token match: {word}'} for x in project_search(project,word,10))
    return {'error':text,'likely_files':candidates[:30],'next_steps':['Inspect the first stack-trace file','Check the related API contract','Run the affected test plan','Apply a reviewed change only after approval']}


def generate_docs(project: ProjectRegistry, target: str, user=None):
    feature = explain_feature(project,target,user)
    lines = [f'# {target} — SO_IAM_OS Codex Documentation','', '## Architecture', 'Request → Frontend → Store/Service → API → Django → Database', '', '## Features']
    lines += [f'- {x["name"]} (`{x["app_label"]}`)' for x in feature['features']]
    lines += ['', '## APIs']
    lines += [f'- `{x["method"]} {x["path"]}` — {x.get("coverage_status")}' for x in feature['apis']]
    lines += ['', '## Files']
    lines += [f'- `{x["path"]}` ({x["kind"]})' for x in feature['files']]
    audit(project,user,'documentation','docs.generate',payload={'target':target}) if user else None
    return {'target':target,'markdown':'\n'.join(lines)}
