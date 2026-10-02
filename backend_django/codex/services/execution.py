from __future__ import annotations
import subprocess
from pathlib import Path
from django.conf import settings
from .intelligence import permission, audit
from ..models import CodexExecutionRequest, ProjectRegistry

ALLOWED = {
    'django.check': ['python', 'manage.py', 'check'],
    'django.test': ['python', 'manage.py', 'test'],
    'frontend.build': ['npm', 'run', 'build'],
    'frontend.test': ['npm', 'run', 'test:unit', '--', '--run'],
    'frontend.lint': ['npm', 'run', 'lint'],
    'git.status': ['git', 'status', '--short'],
    'git.diff': ['git', 'diff', '--stat'],
    'git.log': ['git', 'log', '-5', '--oneline'],
}


def run_safe(user, project: ProjectRegistry, key: str):
    if key not in ALLOWED:
        raise ValueError('Command is not allowlisted.')
    state = permission(project, user, 'RUN_COMMANDS')
    if state != 'ALLOW':
        raise PermissionError(f'RUN_COMMANDS policy is {state}; explicit approval is required.')
    cwd = Path(settings.BASE_DIR)
    if key.startswith('frontend.'):
        cwd = cwd.parent / 'frontend_vue'
    args = ALLOWED[key]
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180, shell=False)
    status = 'success' if result.returncode == 0 else 'failed'
    audit(project, user, 'command', key, status=status, payload={'returncode': result.returncode})
    return {'key': key, 'command': args, 'returncode': result.returncode, 'stdout': result.stdout[-12000:], 'stderr': result.stderr[-12000:], 'status': status}

import hashlib
from django.utils import timezone
from ..models import ChangeSet, CodexChangeFile, ProtectedFeature


def _safe_path(rel):
    root = Path(settings.BASE_DIR).parent.resolve()
    target = (root / rel).resolve()
    if root not in target.parents and target != root:
        raise ValueError('Path escapes project root.')
    if rel.startswith('.env') or '__pycache__' in target.parts:
        raise ValueError('Protected runtime/generated path.')
    return target


def apply_changes(user, project, title, objective, changes, confirm=False):
    if not confirm:
        raise PermissionError('Explicit confirmation is required.')
    state = permission(project, user, 'WRITE_FILES')
    if state != 'ALLOW':
        raise PermissionError(f'WRITE_FILES policy is {state}; set it to ALLOW after explicit user approval.')
    if not isinstance(changes, list) or not changes:
        raise ValueError('changes must be a non-empty list.')
    paths = [str(x.get('path','')).replace('\\','/') for x in changes]
    protected=[]
    for rule in ProtectedFeature.objects.filter(project=project,enabled=True):
        protected += [p for p in rule.paths if any(p==x or x.startswith(p.rstrip('/')+'/') for x in paths)]
    if protected:
        raise PermissionError('Protected paths require explicit protection-rule handling: ' + ', '.join(protected[:10]))
    snapshot = SnapshotService.create(user=user,label=f'Pre-change: {title}')
    cs=ChangeSet.objects.create(project=project,created_by=user,title=title,objective=objective,status='approved',impact={'requested_paths':paths,'snapshot_id':snapshot.id},plan=[{'step':1,'action':'apply reviewed file changes'}],snapshot_id=str(snapshot.id))
    applied=[]
    try:
        for item in changes:
            rel=str(item.get('path','')).replace('\\','/')
            content=item.get('content')
            if not rel or not isinstance(content,str): raise ValueError('Each change requires path and string content.')
            target=_safe_path(rel)
            before=target.read_text(encoding='utf-8',errors='ignore') if target.exists() else ''
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(content,encoding='utf-8')
            before_sha=hashlib.sha256(before.encode('utf-8')).hexdigest() if target.exists() else ''
            after_sha=hashlib.sha256(content.encode('utf-8')).hexdigest()
            CodexChangeFile.objects.create(changeset=cs,path=rel,before_content=before,after_content=content,before_sha256=before_sha,after_sha256=after_sha)
            applied.append(rel)
        cs.status='applied'; cs.diff_summary={'applied':applied}; cs.save(update_fields=['status','diff_summary','updated_at'])
        audit(project,user,'write','changes.apply',payload={'changeset_id':cs.id,'paths':applied})
        return {'changeset_id':cs.id,'snapshot_id':snapshot.id,'status':'applied','paths':applied}
    except Exception:
        for change in cs.file_changes.all():
            target=_safe_path(change.path)
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(change.before_content,encoding='utf-8')
        cs.status='rejected'; cs.save(update_fields=['status','updated_at'])
        audit(project,user,'write','changes.apply',status='rolled_back',payload={'changeset_id':cs.id})
        raise


def rollback_changes(user, project, changeset_id, confirm=False):
    if not confirm: raise PermissionError('Explicit confirmation is required.')
    if permission(project,user,'WRITE_FILES') != 'ALLOW': raise PermissionError('WRITE_FILES policy must be ALLOW.')
    cs=ChangeSet.objects.get(project=project,id=changeset_id)
    for change in cs.file_changes.all():
        target=_safe_path(change.path)
        if change.before_content == '':
            if target.exists(): target.unlink()
        else:
            target.parent.mkdir(parents=True,exist_ok=True); target.write_text(change.before_content,encoding='utf-8')
    cs.status='rolled_back'; cs.save(update_fields=['status','updated_at'])
    audit(project,user,'rollback','changes.rollback',payload={'changeset_id':cs.id})
    return {'changeset_id':cs.id,'status':'rolled_back'}
