"""Offline release validation for the Codex capability contract.
Run from repository root: python scripts/validate_codex_release.py
This intentionally avoids Django/Node runtime dependencies so it can validate the
350 capability contract in CI before installing project dependencies.
"""
from pathlib import Path
import ast, json, re
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'backend_django/codex/catalog.py'
ns={}; exec(compile(ast.parse(CATALOG.read_text(encoding='utf-8')), str(CATALOG), 'exec'), ns)
errors=[]
for name, expected in [('FEATURES',150),('TOOLS',100),('AGENTS',100)]:
    values=ns[name]
    if len(values)!=expected: errors.append(f'{name}: expected {expected}, got {len(values)}')
    keys=[x['key'] for x in values]
    if len(keys)!=len(set(keys)): errors.append(f'{name}: duplicate keys')

for item in ns['FEATURES']:
    required={'key','name','category','purpose','backend','frontend','api','data_model','permissions','ui','integration','tests','status'}
    if not required.issubset(item): errors.append(f"feature contract incomplete: {item.get('key')}")
for item in ns['TOOLS']:
    if not all(item.get(k) for k in ('key','name','category','capability','risk','purpose')): errors.append(f"tool contract incomplete: {item.get('key')}")
for item in ns['AGENTS']:
    if not all(item.get(k) for k in ('key','name','category','purpose','risk')): errors.append(f"agent contract incomplete: {item.get('key')}")
context=ROOT/'project-context/codex-project-context.json'
if not context.exists(): errors.append('missing project-context/codex-project-context.json')
else:
    data=json.loads(context.read_text(encoding='utf-8'))
    for key, expected in [('features',150),('tools',100),('agents',100)]:
        if len(data.get(key,[]))!=expected: errors.append(f'context {key}: invalid count')
urls=(ROOT/'backend_django/codex/urls.py').read_text(encoding='utf-8')
for route in ['registry/features/','registry/tools/','registry/agents/','registry/summary/','registry/health/','registry/validate/','registry/tools/<str:key>/execute/','registry/agents/<str:key>/execute/','context/export/','files/<int:file_id>/content/']:
    if route not in urls: errors.append(f'missing backend route: {route}')
service=(ROOT/'frontend_vue/src/services/codex.js').read_text(encoding='utf-8')
for marker in ['registry.features','registry.tools','registry.agents','registry.validate','executeTool','executeAgent','exportContext','fileContent']:
    if marker not in service: errors.append(f'missing frontend service contract: {marker}')
view=(ROOT/'frontend_vue/src/views/Codex/CodexView.vue').read_text(encoding='utf-8')
if 'CodexCapabilities' not in view: errors.append('CodexCapabilities is not integrated into CodexView')
component=(ROOT/'frontend_vue/src/views/Codex/CodexCapabilities.vue').read_text(encoding='utf-8')
for marker in ['150 Features','100 Tools','100 Agents','Validate All']:
    if marker not in component: errors.append(f'missing UI marker: {marker}')
print('CODEX RELEASE CONTRACT')
print(f"features={len(ns['FEATURES'])} tools={len(ns['TOOLS'])} agents={len(ns['AGENTS'])}")
print('status=PASS' if not errors else 'status=FAIL')
for error in errors: print('ERROR:',error)
raise SystemExit(1 if errors else 0)
