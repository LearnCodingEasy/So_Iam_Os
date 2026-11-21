# ai source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## ai/admin.py
- Type/area: Python module
- Definitions: class AISettingsAdmin(admin.ModelAdmin):; class AIProviderCredentialAdmin(admin.ModelAdmin):; def has_api_key(self, obj):; class AIPromptProfileAdmin(admin.ModelAdmin):; class AIConversationAdmin(admin.ModelAdmin):; class AIMessageAdmin(admin.ModelAdmin):
- Imports (first four): from django.contrib import admin; from .models import AIConversation, AIMessage, AISettings, AIProviderCredential, AIPromptProfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/apps.py
- Type/area: Python module
- Definitions: class AiConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/exceptions.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .services.exceptions import *  # noqa: F401,F403
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/learning_actions.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .services.learning_actions import *  # noqa: F401,F403
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/prompts.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .services.prompts import *  # noqa: F401,F403
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/security.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from .services.security import *  # noqa: F401,F403
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/chat.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .views import AIChatView, AIChatStreamView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/diagnostics.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from ..views import AIHealthView, AICapabilitiesView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path; from ai.api.views import AITopicChatView, AIAgentPlanView, AIChatView, AIConversationDetailView, AIConversationListCreateView, AISettingsView, AIProviderCredentialListCreateView, AIProviderCredentialDetailView, AIBudgetDetailView, AIWorkflowListCreateView, AIWorkflowDetailView, AIWorkflowRunsView, AIProviderModelsView, AIProviderTestView, AIProviderListView, AIUsageView, AIContextInspectView, AIWorkflowValidateView, AITaskProposalView, AIAgentSelectView, AIExecutionListView, AIBudgetListCreateView, AIAuditListView, AIPromptProfileListCreateView, AIPromptProfileDetailView, AILearningPlanPreviewView, AILearningPlanApproveView, AILearningPlanAsyncView, AITaskStatusView, AIFeedbackView, AIHealthView, AICapabilitiesView, AIChatStreamView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/conversations.py
- Type/area: Python API source
- Definitions: class AIMessageSerializer(serializers.ModelSerializer):; class Meta:; class AIConversationSerializer(serializers.ModelSerializer):; class Meta:; class AIChatSerializer(serializers.Serializer):
- Imports (first four): from rest_framework import serializers; from ai.models import AIConversation, AIMessage, AISettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/feedback.py
- Type/area: Python API source
- Definitions: class AIFeedbackSerializer(serializers.Serializer):
- Imports (first four): from rest_framework import serializers
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/learning.py
- Type/area: Python API source
- Definitions: class AILearningTopicSerializer(serializers.Serializer):; class AILearningPlanSerializer(serializers.Serializer):; def validate_topics(self, value):
- Imports (first four): from rest_framework import serializers
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/observability.py
- Type/area: Python API source
- Definitions: class AIExecutionSerializer(serializers.ModelSerializer):; class Meta:; class AIBudgetPolicySerializer(serializers.ModelSerializer):; class Meta:; class AiAuditLogSerializer(serializers.ModelSerializer):; class Meta:; def get_result(self, obj):
- Imports (first four): from rest_framework import serializers; from ai.models import AIExecution, AIBudgetPolicy, AiAuditLog
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/prompts.py
- Type/area: Python API source
- Definitions: class AIPromptProfileSerializer(serializers.ModelSerializer):; class Meta:; def validate_temperature(self, value):; def validate(self, attrs):
- Imports (first four): from rest_framework import serializers; from ai.models import AIPromptProfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/providers.py
- Type/area: Python API source
- Definitions: class AIProviderTestSerializer(serializers.Serializer):; class AIProviderCredentialSerializer(serializers.ModelSerializer):; class Meta:; def to_representation(self, instance):; def _merge_metadata(self, validated_data):; def create(self, validated_data):; def update(self, instance, validated_data):
- Imports (first four): from rest_framework import serializers; from ai.models import AIProviderCredential
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/settings.py
- Type/area: Python API source
- Definitions: class AISettingsSerializer(serializers.ModelSerializer):; class Meta:; def validate_default_prompt_profile(self, value):
- Imports (first four): from rest_framework import serializers; from ai.models import AISettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/workflows.py
- Type/area: Python API source
- Definitions: class AIWorkflowDefinitionSerializer(serializers.ModelSerializer):; class Meta:; def validate_graph(self, value):
- Imports (first four): from rest_framework import serializers; from ai.models import AIWorkflowDefinition; from ai.services.workflow_service import WorkflowService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from ai.api.serializers.conversations import AIMessageSerializer, AIConversationSerializer, AIChatSerializer; from ai.api.serializers.providers import AIProviderTestSerializer, AIProviderCredentialSerializer; from ai.api.serializers.settings import AISettingsSerializer; from ai.api.serializers.prompts import AIPromptProfileSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/views/ai_views.py
- Type/area: Python API source
- Definitions: class AIChatView(APIView):; def post(self, request):; class AIConversationListCreateView(APIView):; def get(self, request):; def post(self, request):; class AIConversationDetailView(APIView):; def get_object(self, request, pk):; def get(self, request, pk):; def delete(self, request, pk):; def post(self, request, pk):; class AISettingsView(APIView):; def get(self, request):; def patch(self, request):; class AIProviderCredentialListCreateView(APIView):; def get(self, request):; def post(self, request):; class AIProviderCredentialDetailView(APIView):; def delete(self, request, provider):; class AIProviderModelsView(APIView):; def get(self, request, provider):; class AIProviderTestView(APIView):; def post(self, request, provider):; class AIProviderListView(APIView):; def get(self, request):; class AIExecutionListView(APIView):; def get(self, request):; class AIBudgetListCreateView(APIView):; def get(self, request):; def post(self, request):; class AIAuditListView(APIView):; def get(self, request):; class AIFeedbackView(APIView):; def post(self, request):; class AIBudgetDetailView(APIView):; def get_object(self, request, pk):; def patch(self, request, pk):; def delete(self, request, pk):; class AIWorkflowListCreateView(APIView):; def get(self, request):; def post(self, request):; class AIWorkflowDetailView(APIView):; def get_object(self, request, pk):; def get(self, request, pk):; def patch(self, request, pk):; def delete(self, request, pk):; class AIWorkflowRunsView(APIView):; def get(self, request, pk):; class AIUsageView(APIView):; def get(self, request):; class AIContextInspectView(APIView):; def get(self, request, pk):; class AIWorkflowValidateView(APIView):; def post(self, request):; class AITaskProposalView(APIView):; def post(self, request):; class AIAgentSelectView(APIView):; def post(self, request):; class AIPromptProfileViewSetMixin:; class AIPromptProfileListCreateView(APIView):; def get(self, request):; def post(self, request):; class AIPromptProfileDetailView(APIView):; def get_object(self, request, pk):; def get(self, request, pk):; def patch(self, request, pk):; def delete(self, request, pk):; class AILearningPlanPreviewView(APIView):; def post(self, request):; class AILearningPlanApproveView(APIView):; def post(self, request):; class AILearningPlanAsyncView(APIView):; def post(self, request):; class AITaskStatusView(APIView):; def get(self, request, task_id):; class AITopicChatView(APIView):; def post(self, request):; class AIAgentPlanView(APIView):; def post(self, request):; class AIHealthView(APIView):; def get(self, request):; class AICapabilitiesView(APIView):; def get(self, request):; class AIChatStreamView(APIView):; def post(self, request):; def replay_stream():; def event_stream():
- Imports (first four): import logging; from rest_framework import status; from rest_framework.decorators import permission_classes; from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .ai_views import logger, AIChatView, AIConversationListCreateView, AIConversationDetailView, AISettingsView, AIProviderCredentialListCreateView, AIProviderCredentialDetailView, AIProviderModelsView, AIProviderTestView, AIProviderListView, AIExecutionListView, AIBudgetListCreateView, AIAuditListView, AIFeedbackView, AIBudgetDetailView, AIWorkflowListCreateView, AIWorkflowDetailView, AIWorkflowRunsView, AIUsageView, AIContextInspectView, AIWorkflowValidateView, AITaskProposalView, AIAgentSelectView, AIPromptProfileViewSetMixin, AIPromptProfileListCreateView, AIPromptProfileDetailView, AILearningPlanPreviewView, AILearningPlanApproveView, AILearningPlanAsyncView, AITaskStatusView, AITopicChatView, AIAgentPlanView, AIHealthView, AICapabilitiesView, AIChatStreamView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0002_aiproviderconfig.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0003_ai_provider_choices.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0004_ai_platform.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0005_rename_ai_aiaudit_user_id_0a9e2c_idx_ai_aiauditl_user_id_5994b6_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0006_remove_aiauditlog_ai_aiauditl_user_id_5994b6_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0007_restore_ai_observability.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0008_alter_aiauditlog_resource_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0009_remove_aiauditlog_ai_aiaudit_user_created_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0010_repair_aiexecution_requested_provider.py
- Type/area: Python migration source
- Definitions: def repair_requested_provider(apps, schema_editor):; class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0011_ai_production_reliability.py
- Type/area: Python migration source
- Definitions: def repair_missing_ai_tables(apps, schema_editor):; def noop_reverse(apps, schema_editor):; class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.constraints
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0012_rename_ai_aibudget_user_id_8b8c65_idx_ai_aibudget_user_id_40709d_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0013_remove_aiauditlog_ai_aiauditl_user_id_5994b6_idx_and_more.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.core.validators; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/0014_aiauditlog.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/audit.py
- Type/area: Python model source
- Definitions: class AiAuditLog(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/budgets.py
- Type/area: Python model source
- Definitions: class AIBudgetPolicy(models.Model):; class Scope(models.TextChoices):; class Meta:; class AIBudgetReservation(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from ..security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/conversations.py
- Type/area: Python model source
- Definitions: class AIConversation(models.Model):; class Meta:; def __str__(self):; class AIMessage(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models; from ..security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/executions.py
- Type/area: Python model source
- Definitions: class AIExecution(models.Model):; class Status(models.TextChoices):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from .conversations import AIConversation; from ..security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/feedback.py
- Type/area: Python model source
- Definitions: class AIFeedback(models.Model):; class Sentiment(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models; from django.core.validators import MinValueValidator, MaxValueValidator
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/prompts.py
- Type/area: Python model source
- Definitions: class AIPromptProfile(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/providers.py
- Type/area: Python model source
- Definitions: class AIProviderCredential(models.Model):; class Meta:; def set_api_key(self, value):; def get_api_key(self):; def has_api_key(self):; class AIProviderConfig(models.Model):; def set_api_key(self, raw_key):; def get_api_key(self):; def api_key(self):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models; from .settings import AISettings; from ..security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/settings.py
- Type/area: Python model source
- Definitions: class AISettings(models.Model):; class Provider(models.TextChoices):; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models; from ..security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/usage.py
- Type/area: Python model source
- Definitions: class AIUsageRecord(models.Model):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/workflows.py
- Type/area: Python model source
- Definitions: class AIWorkflowDefinition(models.Model):; class Meta:; def __str__(self):; class AIWorkflowRun(models.Model):; class Status(models.TextChoices):; class Meta:; def __str__(self):
- Imports (first four): from django.conf import settings; from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .settings import AISettings; from .providers import AIProviderConfig, AIProviderCredential; from .prompts import AIPromptProfile; from .conversations import AIConversation, AIMessage
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/permissions/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from ai.permissions import AIAuthenticatedPermission; from ..services.permissions import AIAuthenticatedPermission
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/base.py
- Type/area: Python module
- Definitions: def _provider_http_error(provider, response):; class BaseAIProvider:; def __init__(self, user=None):; def _configured_value(self, key, default=None):; def _validated_base_url(self, default):; def _request_timeout(self, timeout_seconds=None):; def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def list_models(self):; def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def validate_credentials(self):; def health_check(self):; def get_model_info(self, model):; def estimate_tokens(self, messages):; def calculate_cost(self, *, input_tokens=0, output_tokens=0, model=None):; def _user_api_key(self):
- Imports (first four): import ipaddress; from urllib.parse import urlsplit; import requests; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/deepseek.py
- Type/area: Python module
- Definitions: class DeepSeekProvider(OpenAIProvider):; def __init__(self, user=None):; def list_models(self):
- Imports (first four): import requests; from django.conf import settings; from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError; from .base import BaseAIProvider, _provider_http_error
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/gemini.py
- Type/area: Python module
- Definitions: class GeminiProvider(BaseAIProvider):; def __init__(self, user=None):; def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def list_models(self):
- Imports (first four): import requests; from django.conf import settings; from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError; from .base import BaseAIProvider, _provider_http_error
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/ollama.py
- Type/area: Python module
- Definitions: class OllamaProvider(BaseAIProvider):; def __init__(self, user=None):; def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def list_models(self):
- Imports (first four): import requests; from django.conf import settings; from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError; from .base import BaseAIProvider, _provider_http_error
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/openai.py
- Type/area: Python module
- Definitions: class OpenAIProvider(BaseAIProvider):; def __init__(self, user=None):; def _headers(self):; def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):; def list_models(self):
- Imports (first four): import requests; from django.conf import settings; from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError; from .base import BaseAIProvider, _provider_http_error
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/openrouter.py
- Type/area: Python module
- Definitions: class OpenRouterProvider(OpenAIProvider):; def __init__(self, user=None):; def list_models(self):
- Imports (first four): import requests; from django.conf import settings; from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError; from .base import BaseAIProvider, _provider_http_error
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/providers/__init__.py
- Type/area: Python module
- Definitions: def get_ai_provider(provider_name, user=None):; class AIProviderFallbackChain:; def __init__(self, user=None):; def generate(self, *, provider=None, model=None, messages=None, temperature=None, max_tokens=None, **kwargs):
- Imports (first four): from .base import BaseAIProvider; from .ollama import OllamaProvider; from .openai import OpenAIProvider; from .gemini import GeminiProvider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/agent_executor.py
- Type/area: Python service source
- Definitions: class AgentExecutor:; def __init__(self, user: Any = None):; def execute(
- Imports (first four): from typing import Any; from ..exceptions import AIError; from .core import AIFallbackChainService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/agent_selector.py
- Type/area: Python service source
- Definitions: class AgentSelection:; class AgentSelector:; def select(*, user: Any, message: str = "", provider: str | None = None,
- Imports (first four): from dataclasses import dataclass; from typing import Any; from django.conf import settings; from ..models import AISettings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/audit_service.py
- Type/area: Python service source
- Definitions: class AuditService:; def record(*, user, action, resource="", result="success", execution=None, metadata=None):; def list_for_user(user, limit=100):; def log_event(user, action, resource=None, details=None, ip_address=None):
- Imports (first four): from ..models import AiAuditLog
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/budget_service.py
- Type/area: Python service source
- Definitions: class BudgetService:; def policy(user, scope="user", scope_key=""):; def check(cls, *, user, provider="", agent=""):; def reserve(cls, *, user, estimated_cost=Decimal("0"), estimated_tokens=0,; def settle(cls, reservation, *, actual_cost=None, actual_tokens=None):; def release(cls, reservation):
- Imports (first four): from datetime import timedelta; from decimal import Decimal; from django.db.models import Sum; from django.db import transaction
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/capabilities.py
- Type/area: Python service source
- Definitions: def get_capabilities():
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/context_inspector.py
- Type/area: Python service source
- Definitions: class ContextInspector:; def inspect_conversation(*, user, conversation_id):
- Imports (first four): from ..models import AIConversation
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/context_service.py
- Type/area: Python service source
- Definitions: class ContextService:; def __init__(self,user): self.user=user; def build(self,max_items=20): return AIContextBuilder(self.user,max_items=max_items).build()
- Imports (first four): from .core import AIContextBuilder
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/conversation_service.py
- Type/area: Python service source
- Definitions: class ConversationService:; def list_for_user(user):; def get_for_user(*, user, conversation_id):; def rename(*, user, conversation_id, title):; def history(conversation):
- Imports (first four): from ..models import AIConversation, AIMessage; from ..exceptions import AIError
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/core.py
- Type/area: Python service source
- Definitions: class AIFallbackChainService:; def generate_completion(; def finish_failure(exc):; def stream_completion(; class AIContextBuilder:; def __init__(self, user, max_items=20):; def build(self):; class AIService:; def __init__(self, user):; def get_settings(self):; def resolve_selection(self, conversation, provider=None, model=""):; def should_persist_selection(result_provider, selected_provider):; def create_conversation(self, title="", provider=None, model=""):; def get_or_create_conversation(self, conversation_id=None, provider=None, model=""):; def build_messages(self, conversation, current_message=""):; def execute_learning_action(self, message, provider=None, model=""):; def serialize_learning_result(self, result):; def approve_learning_plan(self, plan):; def chat(self, message, conversation_id=None, provider=None, model="", idempotency_key="", system_prompt="", temperature=None, max_tokens=None):
- Imports (first four): import json; from django.conf import settings; from django.db import transaction; from django.utils import timezone
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/credential_service.py
- Type/area: Python service source
- Definitions: class CredentialService:; def __init__(self,user): self.user=user; def save(self,provider,api_key,metadata=None):; def validate(self,provider,model=''):
- Imports (first four): from django.utils import timezone; from ..models import AIProviderCredential; from ..providers import get_ai_provider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/diagnostics.py
- Type/area: Python service source
- Definitions: class AIDiagnostics:; def __init__(self,user): self.user=user; def run(self):
- Imports (first four): from django.db import connection; from django.conf import settings; from .provider_service import ProviderService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/exceptions.py
- Type/area: Python service source
- Definitions: class AIError(Exception):; def __init__(self, message=None, *, category="unknown", retryable=False):; class AIProviderError(AIError):; def __init__(self, message=None, *, category="provider_error", retryable=True,; class AIConfigurationError(AIError):; def __init__(self, message=None, *, category="configuration_error"):; class AIResponseError(AIError):; def __init__(self, message=None, *, category="invalid_provider_response"):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/execution_service.py
- Type/area: Python service source
- Definitions: class ExecutionService:; def start(*, user, agent="default", task_type="chat", conversation=None,; def finish(obj, *, status="succeeded", provider=None, model=None,
- Imports (first four): import logging; from django.utils import timezone; from django.db import transaction; from ..models import AIExecution, AIUsageRecord, AiAuditLog
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/fallback_service.py
- Type/area: Python service source
- Definitions: class FallbackService:; def __init__(self, user=None, providers=None):; def execute(self, *, messages, model=None, temperature=None, max_tokens=None):
- Imports (first four): import logging; from ..exceptions import AIProviderError, AIResponseError; from .agent_executor import AgentExecutor
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/feedback_service.py
- Type/area: Python service source
- Definitions: class FeedbackService:; def upsert(*, user, message_id, sentiment, reason="", comment="", feedback_category="", rating=None):
- Imports (first four): from ..models import AIFeedback, AIMessage
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/learning_actions.py
- Type/area: Python service source
- Definitions: def looks_like_learning_request(message):; def extract_learning_skill(message):; class AILearningActionService:; def __init__(self, user):; def generate_ai_plan(*, message, provider="ollama", model="", user=None):; def generate_topics(skill_name):; def create_learning_plan(; def _create_topics(self, *, path, skill, topics):
- Imports (first four): from django.db import transaction; from django.utils.text import slugify; from learning.models import (; from learning.services import LearningService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/permissions.py
- Type/area: Python service source
- Definitions: class AIAuthenticatedPermission(IsAuthenticated):
- Imports (first four): from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/prompts.py
- Type/area: Python service source
- Definitions: def build_learning_topic_content_prompt(context):; def build_system_prompt(context=None):; def build_learning_intent_prompt(message):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/prompt_template_service.py
- Type/area: Python service source
- Definitions: class PromptTemplateService:; def list_for_user(user):; def create(*, user, name, system_prompt, context_instructions="", temperature=0.7, max_tokens=2048):
- Imports (first four): from ..models import AIPromptProfile
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/providers.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): from ..providers.base import BaseAIProvider, _provider_http_error; from ..providers.openai import OpenAIProvider; from ..providers.gemini import GeminiProvider; from ..providers.ollama import OllamaProvider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/provider_manager.py
- Type/area: Python service source
- Definitions: class ProviderManager:; def list_for_user(cls, user):; def list_models(*, user, provider):
- Imports (first four): from django.conf import settings; from ..models import AIProviderCredential, AISettings; from ..providers import get_ai_provider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/provider_service.py
- Type/area: Python service source
- Definitions: class ProviderService:; def __init__(self, user):; def provider(self, name):; def health(self, name, force=False):; def models(self, name, force=False):; def test(self, name, model=""):
- Imports (first four): from django.core.cache import cache; from django.conf import settings; from django.utils import timezone; from ..providers import get_ai_provider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/security.py
- Type/area: Python service source
- Definitions: def _fernet(secret):; def _configured_fernet():; def _legacy_fernet():; def validate_encryption_configuration(*, production=False):; def rotate_encryption_key(value, old_key):; def encrypt_secret(value):; def decrypt_secret(value):
- Imports (first four): import base64; import hashlib; from cryptography.fernet import Fernet, InvalidToken; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/task_planner.py
- Type/area: Python service source
- Definitions: class TaskPlanner:; def proposal(*, title: str, description: str = "", steps: list[str] | None = None,
- Imports (first four): from typing import Any
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/tests.py
- Type/area: Python service source
- Definitions: class TaskPlannerTests(SimpleTestCase):; def test_proposal_requires_title_and_confirmation(self):; def test_empty_title_is_rejected(self):; class WorkflowServiceTests(SimpleTestCase):; def test_valid_graph(self):; def test_unknown_edge_endpoint_is_rejected(self):; class AIFallbackResponseTests(TestCase):; def setUp(self):; def test_invalid_primary_response_moves_to_configured_fallback(self):; class Provider:; def __init__(self, name):; def generate(self, **kwargs):; def provider_factory(name, user=None):; class FallbackUserIsolationTests(TestCase):; def setUp(self):; def test_other_users_credentials_are_not_used_as_fallback(self):; class Provider:; def __init__(self, name):; def generate(self, **kwargs):; def factory(name, user=None):; def test_user_credential_is_available_only_to_its_owner(self):; class OpenAIRequestAuthenticationTests(TestCase):; def setUp(self):; def test_openai_request_sends_bearer_header_and_does_not_follow_redirects(self):; def test_openai_401_error_does_not_echo_response_body(self):; class ProviderFailureClassificationTests(TestCase):; def setUp(self):; def test_provider_specific_invalid_request_falls_back(self):; class Provider:; def __init__(self, name):; def generate(self, **kwargs):; def test_quota_exhaustion_is_not_retryable(self):; def test_http_failure_classification_is_safe_and_retry_aware(self):; def test_auth_failure_is_not_retried_for_same_provider(self):
- Imports (first four): from django.test import SimpleTestCase, TestCase; from ai.services.task_planner import TaskPlanner; from ai.services.workflow_service import WorkflowService; from django.contrib.auth import get_user_model
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/usage_service.py
- Type/area: Python service source
- Definitions: class UsageService:; def summarize(*, user=None):
- Imports (first four): from django.db.models import Count; from ..models import AIConversation, AIMessage
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/workflow_service.py
- Type/area: Python service source
- Definitions: class WorkflowService:; def validate(cls, graph):; def visit(node_id):
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/services/__init__.py
- Type/area: Python service source
- Definitions: def __getattr__(name):
- Imports (first four): from importlib import import_module
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tasks/ai_tasks.py
- Type/area: Python task source
- Definitions: def generate_learning_plan(self, user_id, message, provider=None, model=None):
- Imports (first four): from celery import shared_task; from ..services import AIService; from django.contrib.auth import get_user_model; from ..learning_actions import AILearningActionService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tasks/__init__.py
- Type/area: Python task source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_ai.py
- Type/area: Python test source
- Definitions: class AIServiceTests(TestCase):; def setUp(self):; def test_create_conversation(self, mock_provider):; def test_chat_creates_messages(; class AIAPITests(TestCase):; def setUp(self):; def test_chat_endpoint(; class AIFeedbackAPITests(TestCase):; def setUp(self):; def test_feedback_is_saved_and_updated_for_owned_assistant_message(self):; def test_feedback_cannot_reference_another_users_message(self):; class AIPlatformIntegrationTests(TestCase):; def setUp(self):; def test_credential_delete_is_idempotent(self):; def test_workflow_definition_is_user_scoped_and_persisted(self):; def test_invalid_workflow_graph_is_rejected(self):; def test_budget_detail_cannot_modify_another_users_policy(self):; class AIProviderConnectivityTests(TestCase):; def setUp(self):; def test_provider_test_executes_generation_with_selected_model(self, mock_get_provider):; def test_provider_test_rejects_empty_generation(self, mock_get_provider):; def test_provider_test_validates_model_length(self):
- Imports (first four): from unittest.mock import patch; from django.contrib.auth import get_user_model; from django.test import TestCase; from rest_framework.test import APIClient
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_ai_repair_regressions.py
- Type/area: Python test source
- Definitions: class AIModelExportRegressionTests(SimpleTestCase):; def test_budget_reservation_and_audit_models_are_exported(self):; class ProviderEndpointValidationTests(SimpleTestCase):; def test_external_provider_rejects_insecure_private_production_endpoint(self):; class FallbackPolicyRegressionTests(SimpleTestCase):; def test_disabled_fallback_does_not_switch_provider(self):; class FailedProvider:; def generate(self, **kwargs):; class CredentialUpsertRegressionTests(TestCase):; def setUp(self):; def test_updating_api_key_preserves_existing_provider_metadata(self):; class ExecutionAuditRegressionTests(TestCase):; def setUp(self):; def test_execution_lifecycle_writes_to_current_audit_schema(self):; class StreamingFallbackRegressionTests(SimpleTestCase):; def test_stream_falls_back_when_primary_fails_before_first_delta(self):; class Provider:; def __init__(self, name):; def generate_stream(self, **kwargs):; def test_stream_does_not_switch_after_partial_output(self):; class PartialProvider:; def generate_stream(self, **kwargs):; class UserProviderDefaultRegressionTests(TestCase):; def setUp(self):; def test_new_user_settings_inherit_application_provider_default(self):; def test_existing_user_provider_preference_is_not_overwritten(self):; class PreferredProviderErrorPolicyTests(SimpleTestCase):; def test_preferred_provider_authentication_failure_is_not_hidden_by_fallback(self):; class FailedProvider:; def generate(self, **kwargs):; class ProviderConfigurationFallbackTests(SimpleTestCase):; def test_missing_preferred_provider_configuration_uses_available_fallback(self):; class WorkingProvider:; def generate(self, **kwargs):; def provider_factory(name, user=None):; def test_missing_preferred_provider_configuration_is_visible_when_fallback_disabled(self):; def test_streaming_can_fallback_after_preferred_provider_configuration_error(self):; class WorkingStreamProvider:; def generate_stream(self, **kwargs):; def provider_factory(name, user=None):; class AsyncLearningTaskOwnershipTests(TestCase):; def setUp(self):; def test_pending_task_is_visible_only_to_audited_owner(self):; class PendingResult:; def successful():; def failed():; class ChatIdempotencyRegressionTests(TestCase):; def setUp(self):; def test_successful_request_key_replays_saved_assistant_message(self):; def test_running_request_key_is_not_executed_twice(self):
- Imports (first four): from types import SimpleNamespace; from unittest.mock import patch; from django.contrib.auth import get_user_model; from django.test import SimpleTestCase, TestCase, override_settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_credential_security.py
- Type/area: Python test source
- Definitions: class AICredentialEncryptionTests(SimpleTestCase):; def test_dedicated_key_encrypts_and_decrypts_credentials(self):; def test_legacy_secret_key_format_remains_supported(self):; def test_versioned_ciphertext_requires_dedicated_key(self):
- Imports (first four): from django.test import SimpleTestCase, override_settings; from ai.services.security import decrypt_secret, encrypt_secret
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_production_architecture.py
- Type/area: Python test source
- Definitions: class AIArchitectureTests(SimpleTestCase):; def test_capabilities_count(self):; def test_provider_registry(self):; def test_model_package_exports(self):
- Imports (first four): from django.test import SimpleTestCase; from ai.services.capabilities import get_capabilities; from ai.providers import get_ai_provider; from ai.providers.ollama import OllamaProvider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_provider_adapters.py
- Type/area: Python test source
- Definitions: class OpenAIProviderAdapterTests(SimpleTestCase):; def test_reasoning_models_use_max_completion_tokens_without_temperature(self, mock_post):; def test_standard_models_keep_max_tokens_and_temperature(self, mock_post):
- Imports (first four): from unittest.mock import Mock, patch; from django.test import SimpleTestCase, override_settings; from ai.providers.openai import OpenAIProvider
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/test_provider_switching_e2e.py
- Type/area: Python test source
- Definitions: class FakeProviders:; class Handler(BaseHTTPRequestHandler):; def log_message(self, *a):; def _send(self, code, body):; def do_POST(self):; def free_port():; class ProviderSwitchingE2E(APITestCase):; def setUpClass(cls):; def tearDownClass(cls):; def setUp(self):; def add_openai(self, priority=10):; def chat(self, **extra):; def test_01_primary_local_ollama_works(self):; def test_02_primary_down_falls_back_to_openai(self):; def test_03_primary_recovers_after_fallback_in_same_conversation(self):; def test_04_stale_model_from_other_provider_does_not_break_primary(self):; def test_05_fallback_disabled_reports_primary_failure(self):; def test_06_connection_refused_primary_then_fallback(self):; def test_07_invalid_credentials_on_primary_is_not_silently_swallowed(self):; def test_08_all_providers_fail_ends_with_failed_execution_no_loop(self):; def stream(self, **extra):; def test_09_stream_stale_model_recovers_on_primary(self):; def test_10_stream_fallback_does_not_demote_primary(self):
- Imports (first four): import json; import socket; import threading; from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## ai/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

