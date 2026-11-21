# codex services and workflows

## Service/task/signal source


### codex/tasks.py
L5: def run_local_ai_job(self, job_id):

### codex/services/build_workspace.py
L18: def root_for(project):
L35: def safe_path(root, value):
L40: def _find_usage(root, token, limit=80):
L53: def analyze_file(project, rel):
L94: def build_graph(project, rescan=False):
L114: def export_manifest(project):
L162: def _hash_path(root, rel):

### codex/services/capabilities.py
L17: def ensure_capability_catalog(project=None):
L65: def catalog_summary(project):
L75: def _project_root(project):
L80: def execute_tool(project, user, key, payload=None):
L125: def execute_agent(project, user, key, payload=None):
L145: def health_report(project):
L163: def _record(project, user, kind, key, status, input_data, output_data, validation):

### codex/services/change_planner.py
L3: class ChangePlanner:
L5: def plan(*,user,title,objective,paths=None):

### codex/services/context_builder.py
L3: class ContextBuilder:
L5: def build(project):

### codex/services/execution.py
L21: def run_safe(user, project: ProjectRegistry, key: str):
L41: def _safe_path(rel):
L51: def apply_changes(user, project, title, objective, changes, confirm=False):
L98: def rollback_changes(user, project, changeset_id, confirm=False):

### codex/services/extensions.py
L25: def project_root(project: ProjectRegistry) -> Path:
L30: def _safe_relative(root: Path, path: str) -> Path:
L37: def bootstrap_workflow(project: ProjectRegistry):
L46: def verify_workflow(project: ProjectRegistry):
L69: def freeze_item(project, user, payload):
L98: def generate_manifests(project: ProjectRegistry):
L134: def build_prompt(project, prompt_type, goal, paths=None):
L167: def markdown_index(project, path=""):
L185: def local_file_link(project, path):
L193: def architecture_analyze(project, module_path):
L217: def create_local_job(project, user, task_type, input_data):

### codex/services/intelligence.py
L38: def _root() -> Path:
L42: def _read(path: Path) -> str:
L49: def _rel(path: Path) -> str:
L53: def _file_paths():
L66: def ensure_tools(project: ProjectRegistry):
L84: def ensure_policy(project: ProjectRegistry, user=None):
L97: def permission(project, user, key: str) -> str:
L101: def audit(project, user, event_type, action, status='success', payload=None):
L107: def search(project: ProjectRegistry, query: str, limit=50):
L129: def _python_symbols(text: str):
L141: def build_graph(project: ProjectRegistry, refresh=True):
L146: def node(key, kind, label, path='', metadata=None):
L175: def impact(project: ProjectRegistry, query: str, limit=100):
L183: def security_scan(project: ProjectRegistry, user=None):
L200: def duplicate_scan(project: ProjectRegistry, user=None):
L210: def code_review(project: ProjectRegistry, path: str, user=None):
L230: def test_plan(project: ProjectRegistry, target: str, user=None):
L242: def agent_plan(project: ProjectRegistry, request: str, user=None):
L256: def explain_feature(project: ProjectRegistry, query: str, user=None):
L265: def debug_error(project: ProjectRegistry, error_text: str, user=None):
L277: def generate_docs(project: ProjectRegistry, target: str, user=None):

### codex/services/openai_service.py
L11: class OpenAIService:
L27: def analyze(self, *, request, project_context, user=None):

### codex/services/project_context.py
L18: class ProjectContextService:
L20: def __init__(self, project=None):
L25: def build_context(self, query: str):
L100: def _features(self, query):
L125: def _files(self, query):
L149: def _apis(self, query):

### codex/services/project_scanner.py
L9: class ProjectScanner:
L10: def __init__(self, project=None):
L13: def scan_files(self):
L28: def scan_features(self):
L38: def scan_apis(self):
L41: def walk(patterns,prefix=""):
L62: def run(self):

### codex/services/snapshot_service.py
L4: class SnapshotService:
L6: def create(*,user,label):

### codex/services/user_context.py
L11: def _limit(raw_value, default=25, maximum=100):
L19: def build_user_context(user, *, limit=25, include_content=False):

### codex/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
