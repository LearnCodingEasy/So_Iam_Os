"""Codex Build workspace graph, safe project analysis, and immutable manifest helpers."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from ..models import ProjectRegistry, ProtectedItem

STAGES = [
    ("repository", "Repository Setup", "Repository, clone, and workspace", [".git", "README.md"]),
    ("venv", "Virtual Environment", "Python environment and interpreter", ["requirements.txt", ".venv"]),
    ("backend", "Backend Setup", "Django apps, dependencies, and settings", ["backend_django/manage.py", "backend_django/backend_django/settings.py"]),
    ("frontend", "Frontend Setup", "Vue, Vite, PrimeVue, Pinia, and dependencies", ["frontend_vue/package.json", "frontend_vue/src"]),
    ("integration", "Full-Stack Integration", "API bridge, CORS, and routing", ["backend_django/codex/urls.py", "frontend_vue/src/services/codex.js"]),
]
IGNORE = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "media", "staticfiles"}

def root_for(project):
    """Resolve the configured project root, or discover it from the Django layout.

    Never silently assume BASE_DIR.parent is the repository root: in this project
    BASE_DIR is backend_django/backend_django.
    """
    if project.root_path:
        configured = Path(project.root_path).expanduser().resolve()
        if configured.exists() and configured.is_dir():
            return configured
    base = Path(settings.BASE_DIR).resolve()
    for candidate in (base, *base.parents):
        if (candidate / "backend_django" / "manage.py").is_file() and (candidate / "frontend_vue" / "package.json").is_file():
            return candidate
    # Fall back to the Django source root, without pretending it is the repo root.
    return base.parent

def safe_path(root, value):
    p=(root / str(value).replace('\\','/')).resolve()
    if p != root and root not in p.parents: raise ValueError('Path escapes project root.')
    return p

def _find_usage(root, token, limit=80):
    found=[]
    for p in root.rglob('*'):
        if not p.is_file() or any(part in IGNORE for part in p.parts) or p.suffix.lower() not in {'.py','.vue','.js','.ts','.json','.scss','.html','.txt'}: continue
        try:
            if p.stat().st_size > 1_000_000: continue
            for n,line in enumerate(p.read_text(encoding='utf-8',errors='ignore').splitlines(),1):
                if token.lower() in line.lower():
                    found.append({'path':p.relative_to(root).as_posix(),'line':n,'excerpt':line.strip()[:240]})
                    if len(found)>=limit:return found
        except OSError: pass
    return found

def analyze_file(project, rel):
    root=root_for(project); target=safe_path(root,rel)
    if not target.is_file(): raise ValueError('File does not exist.')
    text=target.read_text(encoding='utf-8',errors='ignore')
    lines=text.splitlines(); suffix=target.suffix.lower()
    package={}
    if target.name=='package.json':
        try:
            data=json.loads(text); package={**data.get('dependencies',{}),**data.get('devDependencies',{})}
        except json.JSONDecodeError: pass
    imports=[]
    for i,line in enumerate(lines,1):
        if re.search(r'^\s*(?:import\s|from\s+\S+\s+import|require\()',line): imports.append({'line':i,'text':line.strip()[:240]})
    if target.name.lower() == 'requirements.txt':
        for i, line in enumerate(lines, 1):
            raw = line.strip()
            if raw and not raw.startswith(('#', '-')):
                name = re.split(r'\s*(?:===|==|~=|!=|>=|<=|>|<)\s*', raw, maxsplit=1)[0].strip()
                version_match = re.search(r'(===|==|~=|!=|>=|<=|>|<)\s*([^;\s]+)', raw)
                package[name] = {'specification': raw, 'version_constraint': (version_match.group(2) if version_match else 'unspecified'), 'line': i, 'installed_status': 'declared; runtime installation not verified'}
    dependency_details = []
    if target.name == 'package.json':
        modules_root = root / 'frontend_vue' / 'node_modules'
        for name, version in package.items():
            module_path = modules_root.joinpath(*name.split('/'))
            dependency_details.append({'name': name, 'declared_version': version, 'installed_status': 'installed' if module_path.exists() else 'not found in frontend_vue/node_modules'})
    elif target.name.lower() == 'requirements.txt':
        try:
            from importlib import metadata as importlib_metadata
            for name, info in package.items():
                try: installed_version = importlib_metadata.version(name)
                except importlib_metadata.PackageNotFoundError: installed_version = None
                dependency_details.append({'name': name, 'declared_version': info.get('version_constraint'), 'installed_version': installed_version, 'installed_status': 'installed' if installed_version else 'not found in current Python environment', 'line': info.get('line')})
        except Exception:
            dependency_details = [{'name': name, **info} for name, info in package.items()]
    token=target.stem
    usages=_find_usage(root,token) if len(token)>2 else []
    try: from ..models import FileRegistry; is_protected=FileRegistry.objects.filter(project=project,path=target.relative_to(root).as_posix(),protected=True).exists()
    except Exception: is_protected=False
    return {'path':target.relative_to(root).as_posix(),'absolute_path':str(target),'kind':suffix.lstrip('.') or 'file','size':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'line_count':len(lines),'imports':imports[:100],'dependencies':package,'dependency_details':dependency_details,'usages':usages,'is_locked':is_protected or ProtectedItem.objects.filter(project=project,path=target.relative_to(root).as_posix(),approved=True,frozen=True).exists(),'read_only':True}

def build_graph(project, rescan=False):
    root=root_for(project); protected={x.path for x in ProtectedItem.objects.filter(project=project,approved=True,frozen=True)}
    nodes=[]
    for index,(key,label,description,checks) in enumerate(STAGES):
        existing=[c for c in checks if (root/c).exists() or (root/'backend_django'/c).exists() or (root/'frontend_vue'/c).exists()]
        locked=any(p in protected for p in checks)
        status='ready' if existing and len(existing)==len(checks) else ('incomplete' if existing else 'blocked')
        # File existence is discovery evidence only; it is not execution/test evidence.
        nodes.append({'id':key,'type':'default','position':{'x':80+index*300,'y':100},'data':{'label':label,'description':description,'checks':checks,'found':existing,'status':status,'progress':0,'execution_verified':False,'is_locked':locked,'immutable':locked,'read_only':True}})
    edges=[{'id':f'{STAGES[i][0]}-{STAGES[i+1][0]}','source':STAGES[i][0],'target':STAGES[i+1][0],'type':'smoothstep','animated':True} for i in range(len(STAGES)-1)]
    # Add discovered Django apps and Vue components as informational nodes.
    for folder,kind in [(root/'backend_django','backend'),(root/'frontend_vue'/'src','frontend')]:
        if not folder.exists(): continue
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or any(x in IGNORE for x in p.parts) or p.suffix.lower() not in {'.py','.vue'}: continue
            rel=p.relative_to(root).as_posix()
            if len(nodes)>450: break
            nodes.append({'id':'file:'+rel,'type':'default','position':{'x':80+(len(nodes)%4)*260,'y':260+(len(nodes)//4)*90},'data':{'label':p.name,'description':rel,'path':rel,'status':'discovered','progress':0,'is_locked':rel in protected,'immutable':rel in protected,'read_only':True,'kind':kind}})
    return {'project':project.name,'generated_at':timezone.now().isoformat(),'nodes':nodes,'edges':edges,'read_only':True,'note':'External tools must enforce manifest locks; graph metadata alone is not a filesystem security boundary.'}

def export_manifest(project):
    """Export explicit protection policy and file fingerprints without inventing locks.

    Files being present in the repository or a graph node being discovered does not
    make them protected. Only explicitly approved, frozen registry items are locked.
    """
    root = root_for(project)
    items = []
    for item in ProtectedItem.objects.filter(project=project, approved=True, frozen=True):
        items.append({
            'id': item.key, 'path': item.path, 'type': item.item_type,
            'is_locked': True, 'immutable': True, 'allow_read': True,
            'allow_modify': False, 'allow_delete': False, 'reason': item.reason,
            'sha256': _hash_path(root, item.path),
        })

    fingerprints = []
    for rel in ('README.md', 'requirements.txt', 'frontend_vue/package.json',
                'frontend_vue/package-lock.json', 'frontend_vue/pnpm-lock.yaml',
                'frontend_vue/yarn.lock', 'backend_django/manage.py',
                'backend_django/backend_django/settings.py',
                'backend_django/codex/urls.py'):
        digest = _hash_path(root, rel)
        if digest:
            fingerprints.append({'path': rel, 'algorithm': 'sha256', 'sha256': digest})

    payload = {
        'schema_version': '1.1.0', 'project': project.name,
        'project_key': project.key, 'generated_at': timezone.now().isoformat(),
        'policy': {'locked_items_are_immutable': True, 'reject_modify': True,
                   'reject_delete': True, 'reject_replace': True,
                   'reject_rename': True, 'reject_zip_overwrite': True},
        'protected_items': items, 'file_fingerprints': fingerprints,
        'execution_evidence': [],
        'notes': [
            'Fingerprints detect differences; they do not prove malicious activity.',
            'Only explicitly approved and frozen registry entries are protected.',
            'No build stage is marked passed without recorded execution evidence.',
        ],
    }
    out = root / 'project_build_manifest.json'
    try:
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except OSError:
        # Return the manifest payload even when the repository is read-only.
        pass
    return {'manifest': payload, 'path': str(out), 'download_name': 'project_build_manifest.json'}

def _hash_path(root, rel):
    try:
        p=safe_path(root,rel)
        if p.is_file(): return hashlib.sha256(p.read_bytes()).hexdigest()
    except (ValueError,OSError): pass
    return None
