# ai services and workflows

## Service/task/signal source


### ai/services/agent_executor.py
L7: class AgentExecutor:
L8: def __init__(self, user: Any = None):
L11: def execute(

### ai/services/agent_selector.py
L8: class AgentSelection:
L13: class AgentSelector:
L16: def select(*, user: Any, message: str = "", provider: str | None = None,

### ai/services/audit_service.py
L4: class AuditService:
L6: def record(*, user, action, resource="", result="success", execution=None, metadata=None):
L21: def list_for_user(user, limit=100):
L25: def log_event(user, action, resource=None, details=None, ip_address=None):

### ai/services/budget_service.py
L9: class BudgetService:
L11: def policy(user, scope="user", scope_key=""):
L15: def check(cls, *, user, provider="", agent=""):
L41: def reserve(cls, *, user, estimated_cost=Decimal("0"), estimated_tokens=0,
L73: def settle(cls, reservation, *, actual_cost=None, actual_tokens=None):
L86: def release(cls, reservation):

### ai/services/capabilities.py
L30: def get_capabilities():

### ai/services/context_inspector.py
L3: class ContextInspector:
L5: def inspect_conversation(*, user, conversation_id):

### ai/services/context_service.py
L3: class ContextService:
L4: def __init__(self,user): self.user=user
L5: def build(self,max_items=20): return AIContextBuilder(self.user,max_items=max_items).build()

### ai/services/conversation_service.py
L5: class ConversationService:
L7: def list_for_user(user):
L10: def get_for_user(*, user, conversation_id):
L16: def rename(*, user, conversation_id, title):
L24: def history(conversation):

### ai/services/core.py
L21: class AIFallbackChainService:
L27: def generate_completion(
L134: def finish_failure(exc):
L301: def stream_completion(
L439: class AIContextBuilder:
L440: def __init__(self, user, max_items=20):
L444: def build(self):
L506: class AIService:
L507: def __init__(self, user):
L510: def get_settings(self):
L521: def resolve_selection(self, conversation, provider=None, model=""):
L540: def should_persist_selection(result_provider, selected_provider):
L544: def create_conversation(self, title="", provider=None, model=""):
L551: def get_or_create_conversation(self, conversation_id=None, provider=None, model=""):
L559: def build_messages(self, conversation, current_message=""):
L582: def execute_learning_action(self, message, provider=None, model=""):
L607: def serialize_learning_result(self, result):
L618: def approve_learning_plan(self, plan):
L628: def chat(self, message, conversation_id=None, provider=None, model="", idempotency_key="", system_prompt="", temperature=None, max_tokens=None):

### ai/services/credential_service.py
L5: class CredentialService:
L6: def __init__(self,user): self.user=user
L7: def save(self,provider,api_key,metadata=None):
L11: def validate(self,provider,model=''):

### ai/services/diagnostics.py
L5: class AIDiagnostics:
L6: def __init__(self,user): self.user=user
L7: def run(self):

### ai/services/exceptions.py
L4: class AIError(Exception):
L8: def __init__(self, message=None, *, category="unknown", retryable=False):
L14: class AIProviderError(AIError):
L17: def __init__(self, message=None, *, category="provider_error", retryable=True,
L24: class AIConfigurationError(AIError):
L27: def __init__(self, message=None, *, category="configuration_error"):
L31: class AIResponseError(AIError):
L34: def __init__(self, message=None, *, category="invalid_provider_response"):

### ai/services/execution_service.py
L10: class ExecutionService:
L12: def start(*, user, agent="default", task_type="chat", conversation=None,
L47: def finish(obj, *, status="succeeded", provider=None, model=None,

### ai/services/fallback_service.py
L7: class FallbackService:
L8: def __init__(self, user=None, providers=None):
L11: def execute(self, *, messages, model=None, temperature=None, max_tokens=None):

### ai/services/feedback_service.py
L3: class FeedbackService:
L5: def upsert(*, user, message_id, sentiment, reason="", comment="", feedback_category="", rating=None):

### ai/services/learning_actions.py
L40: def looks_like_learning_request(message):
L58: def extract_learning_skill(message):
L131: class AILearningActionService:
L147: def __init__(self, user):
L151: def generate_ai_plan(*, message, provider="ollama", model="", user=None):
L217: def generate_topics(skill_name):
L364: def create_learning_plan(
L515: def _create_topics(self, *, path, skill, topics):

### ai/services/permissions.py
L4: class AIAuthenticatedPermission(IsAuthenticated):

### ai/services/prompts.py
L228: def build_learning_topic_content_prompt(context):
L236: def build_system_prompt(context=None):
L310: def build_learning_intent_prompt(message):

### ai/services/prompt_template_service.py
L3: class PromptTemplateService:
L5: def list_for_user(user):
L8: def create(*, user, name, system_prompt, context_instructions="", temperature=0.7, max_tokens=2048):

### ai/services/providers.py
No class/function declaration matched the static inventory pattern.

### ai/services/provider_manager.py
L6: class ProviderManager:
L9: def list_for_user(cls, user):
L31: def list_models(*, user, provider):

### ai/services/provider_service.py
L11: class ProviderService:
L12: def __init__(self, user):
L15: def provider(self, name):
L18: def health(self, name, force=False):
L32: def models(self, name, force=False):
L42: def test(self, name, model=""):

### ai/services/security.py
L17: def _fernet(secret):
L26: def _configured_fernet():
L33: def _legacy_fernet():
L40: def validate_encryption_configuration(*, production=False):
L49: def rotate_encryption_key(value, old_key):
L58: def encrypt_secret(value):
L69: def decrypt_secret(value):

### ai/services/task_planner.py
L3: class TaskPlanner:
L5: def proposal(*, title: str, description: str = "", steps: list[str] | None = None,

### ai/services/tests.py
L7: class TaskPlannerTests(SimpleTestCase):
L8: def test_proposal_requires_title_and_confirmation(self):
L14: def test_empty_title_is_rejected(self):
L19: class WorkflowServiceTests(SimpleTestCase):
L20: def test_valid_graph(self):
L27: def test_unknown_edge_endpoint_is_rejected(self):
L35: class AIFallbackResponseTests(TestCase):
L36: def setUp(self):
L41: def test_invalid_primary_response_moves_to_configured_fallback(self):
L47: class Provider:
L48: def __init__(self, name):
L51: def generate(self, **kwargs):
L56: def provider_factory(name, user=None):
L71: class FallbackUserIsolationTests(TestCase):
L72: def setUp(self):
L86: def test_other_users_credentials_are_not_used_as_fallback(self):
L91: class Provider:
L92: def __init__(self, name):
L95: def generate(self, **kwargs):
L98: def factory(name, user=None):
L117: def test_user_credential_is_available_only_to_its_owner(self):
L126: class OpenAIRequestAuthenticationTests(TestCase):
L127: def setUp(self):
L137: def test_openai_request_sends_bearer_header_and_does_not_follow_redirects(self):
L158: def test_openai_401_error_does_not_echo_response_body(self):
L178: class ProviderFailureClassificationTests(TestCase):
L179: def setUp(self):
L185: def test_provider_specific_invalid_request_falls_back(self):
L191: class Provider:
L192: def __init__(self, name):
L195: def generate(self, **kwargs):
L212: def test_quota_exhaustion_is_not_retryable(self):
L225: def test_http_failure_classification_is_safe_and_retry_aware(self):
L240: def test_auth_failure_is_not_retried_for_same_provider(self):

### ai/services/usage_service.py
L4: class UsageService:
L6: def summarize(*, user=None):

### ai/services/workflow_service.py
L2: class WorkflowService:
L5: def validate(cls, graph):
L34: def visit(node_id):

### ai/services/__init__.py
L29: def __getattr__(name):

### ai/tasks/ai_tasks.py
L5: def generate_learning_plan(self, user_id, message, provider=None, model=None):

### ai/tasks/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
