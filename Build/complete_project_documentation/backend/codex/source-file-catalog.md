# codex source-file catalog

All Python files discovered under this installed app are listed, including tests and migrations. Imports and top-level declarations are static extracts; callers are not exhaustively resolved.


## codex/admin.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): from django.contrib import admin; from .models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/apps.py
- Type/area: Python module
- Definitions: class CodexConfig(AppConfig):
- Imports (first four): from django.apps import AppConfig
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/catalog.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/permissions.py
- Type/area: Python module
- Definitions: class CodexAuthenticated(IsAuthenticated):
- Imports (first four): from rest_framework.permissions import IsAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tasks.py
- Type/area: Python module
- Definitions: def run_local_ai_job(self, job_id):
- Imports (first four): from celery import shared_task; from django.utils import timezone; from .models import LocalAIJob, FileRegistry; from .services.extensions import project_root, markdown_index, architecture_analyze
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/urls.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from django.urls import path, include; from rest_framework.routers import DefaultRouter; from codex.api.views import *
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/agent_definition_serializers.py
- Type/area: Python API source
- Definitions: class AgentDefinitionSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import CodexAgentDefinition
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/api_endpoint_serializers.py
- Type/area: Python API source
- Definitions: class APIEndpointSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import APIEndpoint
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/capability_run_serializers.py
- Type/area: Python API source
- Definitions: class CapabilityRunSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import CodexCapabilityRun
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/change_set_serializers.py
- Type/area: Python API source
- Definitions: class ChangeSetSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import ChangeSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/feature_serializers.py
- Type/area: Python API source
- Definitions: class FeatureSerializer(serializers.ModelSerializer):; class Meta:; class FeatureDefinitionSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import Feature, CodexFeatureDefinition
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/file_serializers.py
- Type/area: Python API source
- Definitions: class FileSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import FileRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/local_ai_job_serializers.py
- Type/area: Python API source
- Definitions: class LocalAIJobSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import LocalAIJob
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/project_serializers.py
- Type/area: Python API source
- Definitions: class ProjectSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/protected_feature_serializers.py
- Type/area: Python API source
- Definitions: class ProtectedFeatureSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import ProtectedFeature
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/protected_item_serializers.py
- Type/area: Python API source
- Definitions: class ProtectedItemSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import ProtectedItem
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/snapshot_serializers.py
- Type/area: Python API source
- Definitions: class SnapshotSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import ProjectSnapshot
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/tool_definition_serializers.py
- Type/area: Python API source
- Definitions: class ToolDefinitionSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import CodexToolDefinition
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/workflow_step_serializers.py
- Type/area: Python API source
- Definitions: class WorkflowStepSerializer(serializers.ModelSerializer):; class Meta:
- Imports (first four): from rest_framework import serializers; from codex.models import CodexWorkflowStep
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/serializers/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .project_serializers import ProjectSerializer; from .feature_serializers import FeatureSerializer, FeatureDefinitionSerializer; from .file_serializers import FileSerializer; from .api_endpoint_serializers import APIEndpointSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/agent_definition_views.py
- Type/area: Python API source
- Definitions: class AgentDefinitionViewSet(BaseViewSet):
- Imports (first four): from codex.models import CodexAgentDefinition; from codex.models import CodexAgentDefinition; from codex.api.serializers import AgentDefinitionSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/agent_plan_views.py
- Type/area: Python API source
- Definitions: class AgentPlanView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import agent_plan; from codex.models import CodexAgentRun; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/agent_run_views.py
- Type/area: Python API source
- Definitions: class AgentRunView(APIView):; def get(self, request):
- Imports (first four): from codex.models import CodexAgentRun; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/api_endpoint_views.py
- Type/area: Python API source
- Definitions: class APIEndpointViewSet(ReadOnlyModelViewSet):
- Imports (first four): from rest_framework.viewsets import ReadOnlyModelViewSet; from codex.permissions import CodexAuthenticated; from codex.models import APIEndpoint; from codex.api.serializers import APIEndpointSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/apply_changes_views.py
- Type/area: Python API source
- Definitions: class ApplyChangesView(APIView):; def post(self, request):
- Imports (first four): from codex.services.execution import apply_changes; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/architecture_module_analyzer_views.py
- Type/area: Python API source
- Definitions: class ArchitectureModuleAnalyzerView(APIView):; def post(self, request):
- Imports (first four): from codex.services.extensions import architecture_analyze; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/audit_views.py
- Type/area: Python API source
- Definitions: class AuditView(APIView):; def get(self, request):
- Imports (first four): from codex.models import CodexAuditEvent; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/automation_intent_views.py
- Type/area: Python API source
- Definitions: class AutomationIntentView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import ensure_policy; from codex.models import CodexAuditEvent; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/base_views.py
- Type/area: Python API source
- Definitions: class BaseViewSet(ModelViewSet):
- Imports (first four): from rest_framework.viewsets import ModelViewSet; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/build_manifest_views.py
- Type/area: Python API source
- Definitions: class BuildManifestView(APIView):; def post(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.models import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/build_workspace_views.py
- Type/area: Python API source
- Definitions: class BuildWorkspaceView(APIView):; def get(self, request):
- Imports (first four): from codex.services.intelligence import build_graph; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_agents_views.py
- Type/area: Python API source
- Definitions: class CapabilityAgentsView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from django.db.models import Q; from codex.models import CodexAgentDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_agent_execute_views.py
- Type/area: Python API source
- Definitions: class CapabilityAgentExecuteView(CapabilityRegistryMixin, APIView):; def post(self, request, key):
- Imports (first four): from codex.services.capabilities import execute_agent; from codex.models import CodexAgentDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_bootstrap_views.py
- Type/area: Python API source
- Definitions: class CapabilityBootstrapView(CapabilityRegistryMixin, APIView):; def post(self, request):
- Imports (first four): from codex.services.capabilities import ensure_capability_catalog, catalog_summary; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_features_views.py
- Type/area: Python API source
- Definitions: class CapabilityFeaturesView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from django.db.models import Q; from codex.models import CodexFeatureDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_health_views.py
- Type/area: Python API source
- Definitions: class CapabilityHealthView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from codex.services.capabilities import health_report; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_registry_mixin_views.py
- Type/area: Python API source
- Definitions: class CapabilityRegistryMixin:; def project(self, *, create=False):; def require_project(self):
- Imports (first four): from codex.permissions import CodexAuthenticated; from codex.models import ProjectRegistry; from rest_framework.exceptions import NotFound
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_runs_views.py
- Type/area: Python API source
- Definitions: class CapabilityRunsView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from codex.models import CodexCapabilityRun; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_summary_views.py
- Type/area: Python API source
- Definitions: class CapabilitySummaryView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from codex.services.capabilities import catalog_summary; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_tools_views.py
- Type/area: Python API source
- Definitions: class CapabilityToolsView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from django.db.models import Q; from codex.models import CodexToolDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_tool_execute_views.py
- Type/area: Python API source
- Definitions: class CapabilityToolExecuteView(CapabilityRegistryMixin, APIView):; def post(self, request, key):
- Imports (first four): from codex.services.capabilities import execute_tool; from codex.models import CodexToolDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/capability_validate_views.py
- Type/area: Python API source
- Definitions: class CapabilityValidateView(CapabilityRegistryMixin, APIView):; def post(self, request):
- Imports (first four): from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/change_set_views.py
- Type/area: Python API source
- Definitions: class ChangeSetViewSet(BaseViewSet):
- Imports (first four): from codex.models import ChangeSet; from codex.api.serializers import ChangeSetSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/code_review_views.py
- Type/area: Python API source
- Definitions: class CodeReviewView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import code_review; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/context_views.py
- Type/area: Python API source
- Definitions: class ContextView(APIView):; def get(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.models import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/create_snapshot_views.py
- Type/area: Python API source
- Definitions: class CreateSnapshotView(APIView):; def post(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.api.serializers import SnapshotSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/debug_views.py
- Type/area: Python API source
- Definitions: class DebugView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import debug_error; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/documentation_views.py
- Type/area: Python API source
- Definitions: class DocumentationView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import generate_docs; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/duplicate_scan_views.py
- Type/area: Python API source
- Definitions: class DuplicateScanView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import duplicate_scan; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/explain_feature_views.py
- Type/area: Python API source
- Definitions: class ExplainFeatureView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import explain_feature; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/feature_views.py
- Type/area: Python API source
- Definitions: class FeatureDefinitionViewSet(BaseViewSet):; class FeatureViewSet(BaseViewSet):
- Imports (first four): from codex.models import CodexFeatureDefinition; from codex.models import Feature, CodexFeatureDefinition; from codex.api.serializers import FeatureSerializer, FeatureDefinitionSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/file_content_views.py
- Type/area: Python API source
- Definitions: class FileContentView(CapabilityRegistryMixin, APIView):; def get(self, request, file_id):
- Imports (first four): from pathlib import Path; from codex.models import FileRegistry; from rest_framework.views import APIView; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/file_views.py
- Type/area: Python API source
- Definitions: class FileViewSet(ReadOnlyModelViewSet):
- Imports (first four): from codex.models import FileRegistry; from rest_framework.viewsets import ReadOnlyModelViewSet; from codex.permissions import CodexAuthenticated; from codex.models import FileRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/graph_views.py
- Type/area: Python API source
- Definitions: class GraphView(APIView):; def get(self, request):; def post(self, request):
- Imports (first four): from codex.services.intelligence import build_graph; from codex.models import ArchitectureNode, ArchitectureEdge; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/impact_views.py
- Type/area: Python API source
- Definitions: class ImpactView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import impact as impact_analysis; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/intelligence_bootstrap_views.py
- Type/area: Python API source
- Definitions: class IntelligenceBootstrapView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import build_graph, security_scan, ensure_policy, ensure_tools; from codex.models import CodexTool; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/local_ai_job_views.py
- Type/area: Python API source
- Definitions: class LocalAIJobViewSet(ReadOnlyModelViewSet):; class LocalAIJobsView(APIView):; def get(self, request):; def post(self, request):; class LocalAIJobDetailView(APIView):; def get(self, request, job_id):
- Imports (first four): from codex.services.extensions import create_local_job; from codex.models import LocalAIJob; from rest_framework.views import APIView; from rest_framework.viewsets import ReadOnlyModelViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/local_file_open_views.py
- Type/area: Python API source
- Definitions: class LocalFileOpenView(APIView):; def post(self, request):
- Imports (first four): from codex.services.extensions import local_file_link; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/markdown_navigation_views.py
- Type/area: Python API source
- Definitions: class MarkdownNavigationView(APIView):; def post(self, request):
- Imports (first four): from codex.services.extensions import markdown_index; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/open_ai_codex_views.py
- Type/area: Python API source
- Definitions: class OpenAICodexView(APIView):; def post(self, request):; def _parse_json(value):
- Imports (first four): import json; from pathlib import Path; from codex.services.openai_service import OpenAIService; from codex.services.project_context import ProjectContextService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/overview_views.py
- Type/area: Python API source
- Definitions: class OverviewView(APIView):; def get(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.models import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/plan_change_views.py
- Type/area: Python API source
- Definitions: class PlanChangeView(APIView):; def post(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.api.serializers import ChangeSetSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/policy_views.py
- Type/area: Python API source
- Definitions: class PolicyView(APIView):; def get(self, request):; def patch(self, request):
- Imports (first four): from codex.services.intelligence import ensure_policy; from codex.models import CodexAuditEvent; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/project_context_export_views.py
- Type/area: Python API source
- Definitions: class ProjectContextExportView(CapabilityRegistryMixin, APIView):; def get(self, request):
- Imports (first four): from codex.services.capabilities import health_report; from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/project_views.py
- Type/area: Python API source
- Definitions: class ProjectViewSet(ReadOnlyModelViewSet):
- Imports (first four): from rest_framework.viewsets import ReadOnlyModelViewSet; from codex.permissions import CodexAuthenticated; from codex.models import ProjectRegistry; from codex.api.serializers import ProjectSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/prompt_generator_views.py
- Type/area: Python API source
- Definitions: class PromptGeneratorView(APIView):; def post(self, request):
- Imports (first four): from codex.services.extensions import build_prompt; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/protected_feature_views.py
- Type/area: Python API source
- Definitions: class ProtectedFeatureViewSet(BaseViewSet):
- Imports (first four): from codex.models import ProtectedFeature; from codex.api.serializers import ProtectedFeatureSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/protected_item_views.py
- Type/area: Python API source
- Definitions: class ProtectedItemViewSet(BaseViewSet):; def perform_update(self, serializer):; def perform_destroy(self, instance):
- Imports (first four): from codex.models import ProtectedItem; from codex.models import ProtectedItem; from codex.api.serializers import ProtectedItemSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/protected_manifest_views.py
- Type/area: Python API source
- Definitions: class ProtectedManifestView(APIView):; def get(self, request):; def post(self, request):
- Imports (first four): from codex.services.extensions import generate_manifests; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/protected_registry_views.py
- Type/area: Python API source
- Definitions: class ProtectedRegistryView(APIView):; def get(self, request):; def post(self, request):
- Imports (first four): from codex.services.extensions import freeze_item; from codex.models import ProtectedItem; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/rollback_views.py
- Type/area: Python API source
- Definitions: class RollbackView(APIView):; def post(self, request, changeset_id):
- Imports (first four): from codex.services.execution import rollback_changes; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/safe_commands_views.py
- Type/area: Python API source
- Definitions: class SafeCommandsView(APIView):; def get(self, request):; def post(self, request):
- Imports (first four): from codex.services.execution import ALLOWED, run_safe; from codex.services.intelligence import ensure_policy; from codex.models import CodexAuditEvent; from rest_framework.views import APIView
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/scan_views.py
- Type/area: Python API source
- Definitions: class ScanView(APIView):; def post(self, request):
- Imports (first four): from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated; from codex.services.project_scanner import ProjectScanner
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/search_views.py
- Type/area: Python API source
- Definitions: class SearchView(APIView):; def get(self, request):
- Imports (first four): from codex.services.intelligence import search as project_search; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/security_scan_views.py
- Type/area: Python API source
- Definitions: class SecurityScanView(APIView):; def post(self, request):; def get(self, request):
- Imports (first four): from codex.services.intelligence import security_scan; from codex.models import CodexFinding; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/selected_files_context_views.py
- Type/area: Python API source
- Definitions: class SelectedFilesContextView(APIView):; def post(self, request):
- Imports (first four): from pathlib import Path; from rest_framework.views import APIView; from django.conf import settings; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/snapshot_views.py
- Type/area: Python API source
- Definitions: class SnapshotViewSet(ReadOnlyModelViewSet):
- Imports (first four): from rest_framework.viewsets import ReadOnlyModelViewSet; from codex.permissions import CodexAuthenticated; from codex.models import ProjectSnapshot; from codex.api.serializers import SnapshotSerializer
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/test_plan_views.py
- Type/area: Python API source
- Definitions: class TestPlanView(APIView):; def post(self, request):
- Imports (first four): from codex.services.intelligence import test_plan; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/tools_views.py
- Type/area: Python API source
- Definitions: class ToolsView(APIView):; def get(self, request):
- Imports (first four): from codex.services.intelligence import ensure_tools; from codex.models import CodexTool; from rest_framework.views import APIView; from rest_framework.response import Response
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/tool_definition_views.py
- Type/area: Python API source
- Definitions: class ToolDefinitionViewSet(BaseViewSet):
- Imports (first four): from codex.models import CodexToolDefinition; from codex.models import CodexToolDefinition; from codex.api.serializers import ToolDefinitionSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/workflow_step_views.py
- Type/area: Python API source
- Definitions: class WorkflowStepViewSet(BaseViewSet):
- Imports (first four): from codex.models import CodexWorkflowStep; from codex.models import CodexWorkflowStep; from codex.api.serializers import WorkflowStepSerializer; from codex.api.views.base_views import BaseViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/workflow_views.py
- Type/area: Python API source
- Definitions: class WorkflowView(APIView):; def get(self, request):; def post(self, request):
- Imports (first four): from codex.services.extensions import bootstrap_workflow, verify_workflow; from rest_framework.views import APIView; from rest_framework.response import Response; from codex.permissions import CodexAuthenticated
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/api/views/__init__.py
- Type/area: Python API source
- Definitions: none matched
- Imports (first four): from .base_views import BaseViewSet; from .feature_views import FeatureDefinitionViewSet, FeatureViewSet; from .tool_definition_views import ToolDefinitionViewSet; from .agent_definition_views import AgentDefinitionViewSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/commands/codex_bootstrap_governance.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def handle(self, *args, **options):
- Imports (first four): from django.core.management.base import BaseCommand; from codex.models import ProjectRegistry; from codex.services.extensions import bootstrap_workflow, generate_manifests
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/commands/codex_export_context.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def handle(self, *args, **options):
- Imports (first four): import json; from pathlib import Path; from django.core.management.base import BaseCommand; from codex.models import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/commands/codex_scan.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def handle(self,*args,**kwargs): self.stdout.write(str(ProjectScanner().run()))
- Imports (first four): from django.core.management.base import BaseCommand; from codex.services.project_scanner import ProjectScanner
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/commands/codex_seed_capabilities.py
- Type/area: Python module
- Definitions: class Command(BaseCommand):; def handle(self, *args, **options):
- Imports (first four): from django.core.management.base import BaseCommand; from codex.models import ProjectRegistry; from codex.services.capabilities import ensure_capability_catalog, catalog_summary
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/management/commands/__init__.py
- Type/area: Python module
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/0001_initial.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): import django.db.models.deletion; from django.conf import settings; from django.db import migrations, models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/0002_codexconversation_codexanalysis_codexmessage.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/0003_codex_intelligence.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.db import migrations
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/0004_codex_capability_registry.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/0005_codex_protection_workflow_localai.py
- Type/area: Python migration source
- Definitions: class Migration(migrations.Migration):
- Imports (first four): from django.conf import settings; from django.db import migrations, models; import django.db.models.deletion
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/migrations/__init__.py
- Type/area: Python migration source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/api_endpoint.py
- Type/area: Python model source
- Definitions: class APIEndpoint(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/architecture_edge.py
- Type/area: Python model source
- Definitions: class ArchitectureEdge(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.architecture_node import ArchitectureNode; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/architecture_node.py
- Type/area: Python model source
- Definitions: class ArchitectureNode(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/change_set.py
- Type/area: Python model source
- Definitions: class ChangeSet(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_agent_definition.py
- Type/area: Python model source
- Definitions: class CodexAgentDefinition(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_agent_run.py
- Type/area: Python model source
- Definitions: class CodexAgentRun(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_analysis.py
- Type/area: Python model source
- Definitions: class CodexAnalysis(models.Model):
- Imports (first four): from django.db import models; from codex.models.codex_conversation import CodexConversation
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_audit_event.py
- Type/area: Python model source
- Definitions: class CodexAuditEvent(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_capability_run.py
- Type/area: Python model source
- Definitions: class CodexCapabilityRun(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_change_file.py
- Type/area: Python model source
- Definitions: class CodexChangeFile(models.Model):
- Imports (first four): from django.db import models; from codex.models.change_set import ChangeSet
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_conversation.py
- Type/area: Python model source
- Definitions: class CodexConversation(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_execution_request.py
- Type/area: Python model source
- Definitions: class CodexExecutionRequest(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_feature_definition.py
- Type/area: Python model source
- Definitions: class CodexFeatureDefinition(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_finding.py
- Type/area: Python model source
- Definitions: class CodexFinding(models.Model):
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_message.py
- Type/area: Python model source
- Definitions: class CodexMessage(models.Model):
- Imports (first four): from django.db import models; from codex.models.codex_conversation import CodexConversation
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_policy.py
- Type/area: Python model source
- Definitions: class CodexPolicy(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_tool.py
- Type/area: Python model source
- Definitions: class CodexTool(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_tool_definition.py
- Type/area: Python model source
- Definitions: class CodexToolDefinition(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/codex_workflow_step.py
- Type/area: Python model source
- Definitions: class CodexWorkflowStep(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/feature.py
- Type/area: Python model source
- Definitions: class Feature(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/file_registry.py
- Type/area: Python model source
- Definitions: class FileRegistry(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/local_ai_job.py
- Type/area: Python model source
- Definitions: class LocalAIJob(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/project_registry.py
- Type/area: Python model source
- Definitions: class ProjectRegistry(models.Model):
- Imports (first four): from django.db import models
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/project_snapshot.py
- Type/area: Python model source
- Definitions: class ProjectSnapshot(models.Model):
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/protected_feature.py
- Type/area: Python model source
- Definitions: class ProtectedFeature(models.Model):; class Meta:
- Imports (first four): from django.db import models; from codex.models.feature import Feature; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/protected_item.py
- Type/area: Python model source
- Definitions: class ProtectedItem(models.Model):; class Meta:
- Imports (first four): from django.conf import settings; from django.db import models; from codex.models.project_registry import ProjectRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/models/__init__.py
- Type/area: Python model source
- Definitions: none matched
- Imports (first four): from .project_registry import ProjectRegistry; from .feature import Feature; from .file_registry import FileRegistry; from .api_endpoint import APIEndpoint
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/build_workspace.py
- Type/area: Python service source
- Definitions: def root_for(project):; def safe_path(root, value):; def _find_usage(root, token, limit=80):; def analyze_file(project, rel):; def build_graph(project, rescan=False):; def export_manifest(project):; def _hash_path(root, rel):
- Imports (first four): from __future__ import annotations; import hashlib, json, re; from pathlib import Path; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/capabilities.py
- Type/area: Python service source
- Definitions: def ensure_capability_catalog(project=None):; def catalog_summary(project):; def _project_root(project):; def execute_tool(project, user, key, payload=None):; def execute_agent(project, user, key, payload=None):; def health_report(project):; def _record(project, user, kind, key, status, input_data, output_data, validation):
- Imports (first four): from pathlib import Path; from django.conf import settings; from django.utils import timezone; from ..catalog import FEATURES, TOOLS, AGENTS, CATALOG_VERSION
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/change_planner.py
- Type/area: Python service source
- Definitions: class ChangePlanner:; def plan(*,user,title,objective,paths=None):
- Imports (first four): from ..models import ChangeSet,ProjectRegistry,ProtectedFeature
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/context_builder.py
- Type/area: Python service source
- Definitions: class ContextBuilder:; def build(project):
- Imports (first four): from ..models import ProjectRegistry,Feature,FileRegistry,APIEndpoint,ProtectedFeature,ProtectedItem,CodexWorkflowStep,ArchitectureNode,ArchitectureEdge,CodexPolicy,CodexTool,CodexFinding
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/execution.py
- Type/area: Python service source
- Definitions: def run_safe(user, project: ProjectRegistry, key: str):; def _safe_path(rel):; def apply_changes(user, project, title, objective, changes, confirm=False):; def rollback_changes(user, project, changeset_id, confirm=False):
- Imports (first four): from __future__ import annotations; import subprocess; from pathlib import Path; from django.conf import settings
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/extensions.py
- Type/area: Python service source
- Definitions: def project_root(project: ProjectRegistry) -> Path:; def _safe_relative(root: Path, path: str) -> Path:; def bootstrap_workflow(project: ProjectRegistry):; def verify_workflow(project: ProjectRegistry):; def freeze_item(project, user, payload):; def generate_manifests(project: ProjectRegistry):; def build_prompt(project, prompt_type, goal, paths=None):; def markdown_index(project, path=""):; def local_file_link(project, path):; def architecture_analyze(project, module_path):; def create_local_job(project, user, task_type, input_data):
- Imports (first four): from __future__ import annotations; import json; import re; from pathlib import Path
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/intelligence.py
- Type/area: Python service source
- Definitions: def _root() -> Path:; def _read(path: Path) -> str:; def _rel(path: Path) -> str:; def _file_paths():; def ensure_tools(project: ProjectRegistry):; def ensure_policy(project: ProjectRegistry, user=None):; def permission(project, user, key: str) -> str:; def audit(project, user, event_type, action, status='success', payload=None):; def search(project: ProjectRegistry, query: str, limit=50):; def _python_symbols(text: str):; def build_graph(project: ProjectRegistry, refresh=True):; def node(key, kind, label, path='', metadata=None):; def impact(project: ProjectRegistry, query: str, limit=100):; def security_scan(project: ProjectRegistry, user=None):; def duplicate_scan(project: ProjectRegistry, user=None):; def code_review(project: ProjectRegistry, path: str, user=None):; def test_plan(project: ProjectRegistry, target: str, user=None):; def agent_plan(project: ProjectRegistry, request: str, user=None):; def explain_feature(project: ProjectRegistry, query: str, user=None):; def debug_error(project: ProjectRegistry, error_text: str, user=None):; def generate_docs(project: ProjectRegistry, target: str, user=None):
- Imports (first four): from __future__ import annotations; import ast; import hashlib; import re
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/openai_service.py
- Type/area: Python service source
- Definitions: class OpenAIService:; def analyze(self, *, request, project_context, user=None):
- Imports (first four): from django.conf import settings; from ai.models import AISettings; from ai.services.core import AIFallbackChainService
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/project_context.py
- Type/area: Python service source
- Definitions: class ProjectContextService:; def __init__(self, project=None):; def build_context(self, query: str):; def _features(self, query):; def _files(self, query):; def _apis(self, query):
- Imports (first four): from django.db.models import Q; from ..models import (
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/project_scanner.py
- Type/area: Python service source
- Definitions: class ProjectScanner:; def __init__(self, project=None):; def scan_files(self):; def scan_features(self):; def scan_apis(self):; def walk(patterns,prefix=""):; def run(self):
- Imports (first four): from pathlib import Path; import hashlib; from django.conf import settings; from django.urls import get_resolver
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/snapshot_service.py
- Type/area: Python service source
- Definitions: class SnapshotService:; def create(*,user,label):
- Imports (first four): from django.utils.timezone import now; from ..models import ProjectRegistry,ProjectSnapshot,FileRegistry
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/user_context.py
- Type/area: Python service source
- Definitions: def _limit(raw_value, default=25, maximum=100):; def build_user_context(user, *, limit=25, include_content=False):
- Imports (first four): from __future__ import annotations; from django.utils import timezone; from goals.models import Goal; from tasks.models import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/services/__init__.py
- Type/area: Python service source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/test_build_workspace.py
- Type/area: Python test source
- Definitions: class BuildWorkspaceSafetyTests(TestCase):; def test_safe_path_rejects_traversal(self):; def test_build_graph_never_calls_file_presence_execution_success(self):; def test_root_discovery_finds_repository_root(self):; class BuildWorkspaceURLContractTests(TestCase):; def test_public_workspace_route_is_resolvable(self):; def test_public_manifest_route_is_resolvable(self):
- Imports (first four): import hashlib; import json; import tempfile; from pathlib import Path
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/test_capability_registry.py
- Type/area: Python test source
- Definitions: class CapabilityRegistryTests(TestCase):; def setUp(self):; def test_catalog_has_exact_requested_counts(self):; def test_catalog_keys_are_unique(self):; def test_every_tool_has_executable_contract(self):; def test_every_agent_has_executable_contract(self):; def test_summary_matches_contract(self):
- Imports (first four): from django.test import TestCase; from codex.catalog import FEATURES, TOOLS, AGENTS; from codex.models import ProjectRegistry, CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition; from codex.services.capabilities import ensure_capability_catalog, execute_tool, execute_agent, catalog_summary
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/test_extensions.py
- Type/area: Python test source
- Definitions: class CodexExtensionTests(TestCase):; def setUp(self):; def test_workflow_bootstrap_has_five_gated_steps(self):; def test_protected_item_is_frozen(self):; def test_prompt_contains_governance_contract(self):
- Imports (first four): from django.contrib.auth import get_user_model; from django.test import TestCase; from codex.models import ProjectRegistry, ProtectedItem, CodexWorkflowStep, LocalAIJob; from codex.services.extensions import bootstrap_workflow, freeze_item, build_prompt
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/test_foundation.py
- Type/area: Python test source
- Definitions: class CodexFoundationModelTests(TestCase):; def test_registry_constraints_and_api_frontend_place(self):
- Imports (first four): from django.test import TestCase; from codex.models import ProjectRegistry,Feature,APIEndpoint
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/test_user_context.py
- Type/area: Python test source
- Definitions: class UserContextExportTests(TestCase):; def setUp(self):; def test_export_is_scoped_to_authenticated_user(self):; def test_content_is_opt_in_and_bounded(self):
- Imports (first four): from django.test import TestCase; from users_accounts.models import User; from goals.models import Goal; from tasks.models import Task
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.


## codex/tests/__init__.py
- Type/area: Python test source
- Definitions: none matched
- Imports (first four): none matched
- Consumers/callers: not exhaustively resolved; use repository-wide symbol search.

