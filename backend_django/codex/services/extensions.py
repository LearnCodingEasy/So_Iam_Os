from __future__ import annotations

import json
import re
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from ..models import (
    ProjectRegistry, ProtectedItem, ProtectedFeature, CodexWorkflowStep,
    LocalAIJob, FileRegistry, APIEndpoint,
)


WORKFLOW = [
    ("library_setup", "Library Setup", "Verify required frontend/backend libraries exist in package and requirements manifests.", ["package.json", "requirements.txt"]),
    ("configuration", "Configuration", "Verify Django settings, Vue environment, API base URL, authentication and routing configuration.", ["settings.py", "frontend_vue/src/services/api.js"]),
    ("core_code", "Core Code", "Verify Codex models, serializers, services and views are syntactically and structurally present.", ["backend_django/codex/models.py", "backend_django/codex/views.py"]),
    ("integration", "Integration", "Verify Codex routes are represented by frontend service bindings and the project context is available.", ["backend_django/codex/urls.py", "frontend_vue/src/services/codex.js"]),
    ("testing", "Testing", "Run or record available static/runtime verification checks.", ["scripts/validate_codex_release.py"]),
]


def project_root(project: ProjectRegistry) -> Path:
    configured = (project.root_path or "").strip()
    return Path(configured or Path(settings.BASE_DIR).parent).resolve()


def _safe_relative(root: Path, path: str) -> Path:
    target = (root / str(path).replace("\\", "/")).resolve()
    if target != root and root not in target.parents:
        raise ValueError("Path escapes the project root.")
    return target


def bootstrap_workflow(project: ProjectRegistry):
    for index, (key, name, description, checks) in enumerate(WORKFLOW, 1):
        CodexWorkflowStep.objects.update_or_create(
            project=project, key=key,
            defaults={"name": name, "order": index, "description": description, "checks": checks},
        )
    return verify_workflow(project)


def verify_workflow(project: ProjectRegistry):
    root = project_root(project)
    rows = []
    previous_ok = True
    for step in CodexWorkflowStep.objects.filter(project=project).order_by("order"):
        evidence = {}
        for check in step.checks:
            candidates = [root / check, root / "backend_django" / check, root / "frontend_vue" / check]
            exists = any(p.exists() for p in candidates)
            evidence[check] = {"exists": exists, "path": str(next((p for p in candidates if p.exists()), candidates[0]))}
        ok = all(item["exists"] for item in evidence.values()) if evidence else True
        if not previous_ok and ok:
            ok = False
        new_status = "completed" if ok else ("blocked" if not previous_ok else "pending")
        step.status = new_status
        step.evidence = evidence
        step.completed_at = timezone.now() if ok else None
        step.save(update_fields=["status", "evidence", "completed_at", "updated_at"])
        previous_ok = ok
        rows.append({"id": step.id, "key": step.key, "name": step.name, "order": step.order, "status": step.status, "checks": step.checks, "evidence": evidence})
    return {"steps": rows, "completed": sum(x["status"] == "completed" for x in rows), "total": len(rows)}


def freeze_item(project, user, payload):
    key = str(payload.get("key", "")).strip()
    if not key:
        raise ValueError("key is required.")
    path = str(payload.get("path", "")).replace("\\", "/")
    target = str(payload.get("target", "")).strip()
    existing = ProtectedItem.objects.filter(project=project, key=key).first()
    if existing and existing.frozen:
        requested_path = str(payload.get("path", "")).replace("\\", "/")
        if requested_path and existing.path != requested_path:
            raise PermissionError("A frozen ProtectedItem cannot be retargeted.")
    item, _ = ProtectedItem.objects.update_or_create(
        project=project, key=key,
        defaults={
            "item_type": payload.get("item_type", "file"),
            "path": path,
            "target": target,
            "reason": payload.get("reason", "Approved Codex protected item."),
            "approved": True,
            "frozen": True,
            "rules": payload.get("rules", {"allow_read": True, "allow_modify": False, "allow_delete": False}),
            "metadata": payload.get("metadata", {}),
            "approved_by": user,
            "approved_at": timezone.now(),
        },
    )
    return item


def generate_manifests(project: ProjectRegistry):
    root = project_root(project)
    items = []
    for item in ProtectedItem.objects.filter(project=project, approved=True, frozen=True):
        items.append({
            "key": item.key, "type": item.item_type, "path": item.path,
            "target": item.target, "reason": item.reason, "rules": item.rules,
        })
    for item in ProtectedFeature.objects.filter(project=project, enabled=True):
        for path in item.paths or []:
            items.append({
                "key": item.key, "type": "protected_feature", "path": path,
                "target": item.key, "reason": item.reason,
                "rules": item.rules or {"allow_modify": False, "allow_delete": False},
            })
    unique = {(x["key"], x["path"], x["type"]): x for x in items}
    protected = list(unique.values())
    instructions = [
        "This manifest is authoritative Codex governance metadata.",
        "External AI systems MUST NOT modify, replace, rename, move, or delete protected paths/items.",
        "Read-only inspection is allowed unless a protected item's rules explicitly say otherwise.",
        "Any proposed change touching a protected item requires explicit human approval and a reviewed change set.",
        "Do not silently regenerate or replace this manifest while processing a ZIP/project upload.",
    ]
    payload = {
        "version": "1.0.0",
        "project": project.name,
        "generated_at": timezone.now().isoformat(),
        "protected_items": protected,
        "external_ai_instructions": instructions,
    }
    for filename in ("PROJECT_CONTEXT.json", "project_manifest.json"):
        (root / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"files": ["PROJECT_CONTEXT.json", "project_manifest.json"], "protected_count": len(protected), "manifest": payload}


def build_prompt(project, prompt_type, goal, paths=None):
    paths = paths or []
    context = "\n".join(f"- {p}" for p in paths) or "- Relevant files discovered by Codex"
    common = """You are working inside SO_IAM_OS / Codex.
Preserve existing working functionality. Inspect before modifying. Never delete, replace, or bypass protected items.
Use existing Django REST APIs, Vue 3 Composition API, Pinia, PrimeVue and Axios services.
Return an impact analysis, implementation plan, exact files, API/data-contract changes, tests, rollback plan and acceptance criteria."""
    if prompt_type == "bug":
        task = "Diagnose and safely fix the following bug. Identify root cause, affected layers, regression risk, and verification steps."
    elif prompt_type == "image":
        task = "Generate a detailed UI/UX rendering prompt for the Codex interface, including layout, hierarchy, components, states, responsive behavior and accessibility."
    else:
        task = "Design and implement the requested feature with minimal safe changes and complete frontend/backend integration."
    return f"""{common}

TASK TYPE: {prompt_type}
GOAL:
{goal.strip() or "Improve the requested Codex capability."}

SELECTED CONTEXT:
{context}

OUTPUT REQUIREMENTS:
1. Understand current implementation before proposing changes.
2. Respect PROJECT_CONTEXT.json and project_manifest.json governance.
3. Reuse existing endpoints/services/components where possible.
4. Define request/response schemas and UI states.
5. Include tests for happy path, validation failures, permissions and regression.
6. Do not claim a dependency is installed unless verified from the project manifests.
7. Produce production-ready code only after the above analysis.
"""


def markdown_index(project, path=""):
    root = project_root(project)
    base = _safe_relative(root, path) if path else root
    if not base.is_dir():
        raise ValueError("Markdown directory does not exist.")
    rows = []
    for p in sorted(base.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding="utf-8", errors="ignore")
        headings = []
        for line in text.splitlines():
            match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
            if match:
                headings.append({"title": match.group(1), "level": len(line) - len(line.lstrip("#"))})
        rows.append({"path": rel, "title": p.stem, "headings": headings[:100], "size": p.stat().st_size})
    return {"root": str(base), "files": rows, "count": len(rows)}


def local_file_link(project, path):
    root = project_root(project)
    target = _safe_relative(root, path)
    if not target.is_file():
        raise ValueError("File does not exist.")
    return {"path": target.relative_to(root).as_posix(), "absolute_path": str(target), "file_url": target.as_uri()}


def architecture_analyze(project, module_path):
    root = project_root(project)
    target = _safe_relative(root, module_path)
    if not target.exists():
        raise ValueError("Module path does not exist.")
    prefix = target.relative_to(root).as_posix().rstrip("/")
    files = list(FileRegistry.objects.filter(project=project, path__startswith=prefix).values("path", "kind", "app_label", "protected"))
    apis = list(APIEndpoint.objects.filter(project=project, source__icontains=prefix.split("/")[-1]).values("method", "path", "name", "app_label", "frontend_service"))
    models, views, components = [], [], []
    for row in files:
        if row["path"].endswith("models.py"): models.append(row["path"])
        if row["path"].endswith("views.py"): views.append(row["path"])
        if row["kind"] == "vue": components.append(row["path"])
    return {
        "module": prefix, "files": files, "models": models, "views": views,
        "components": components, "apis": apis,
        "suggestions": [
            "Keep API contracts centralized in frontend_vue/src/services/codex.js.",
            "Keep protected paths read-only unless an approved ChangeSet explicitly authorizes a change.",
            "Add integration tests for each frontend-to-Django contract touched by the module.",
        ],
    }


def create_local_job(project, user, task_type, input_data):
    job = LocalAIJob.objects.create(project=project, user=user, task_type=task_type, input_data=input_data or {}, status="queued", provider="local")
    try:
        from ..tasks import run_local_ai_job
        transaction.on_commit(lambda: run_local_ai_job.delay(job.id))
    except Exception:
        # Queueing remains durable; a worker can process the job later.
        pass
    return job
