from rest_framework.views import APIView
from django.conf import settings
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import CodexAuthenticated
from .models import (
    ProjectRegistry, Feature, FileRegistry, APIEndpoint, ProtectedFeature,
    ChangeSet, ProjectSnapshot, CodexFeatureDefinition, CodexToolDefinition,
    CodexAgentDefinition, ProtectedItem, CodexWorkflowStep, LocalAIJob,
)
from .serializers import (
    ProjectSerializer, FeatureSerializer, FileSerializer, APIEndpointSerializer,
    ProtectedFeatureSerializer, ChangeSetSerializer, SnapshotSerializer,
    ProtectedItemSerializer, WorkflowStepSerializer, LocalAIJobSerializer,
    FeatureDefinitionSerializer, ToolDefinitionSerializer, AgentDefinitionSerializer,
)
from .services.project_scanner import ProjectScanner
from .services.context_builder import ContextBuilder
from .services.change_planner import ChangePlanner
from .services.snapshot_service import SnapshotService

class BaseViewSet(ModelViewSet): permission_classes=[CodexAuthenticated]

class FeatureDefinitionViewSet(BaseViewSet):
    queryset = CodexFeatureDefinition.objects.all()
    serializer_class = FeatureDefinitionSerializer
    filterset_fields = ["project", "category", "status", "enabled"]


class ToolDefinitionViewSet(BaseViewSet):
    queryset = CodexToolDefinition.objects.all()
    serializer_class = ToolDefinitionSerializer
    filterset_fields = ["project", "category", "risk", "enabled"]


class AgentDefinitionViewSet(BaseViewSet):
    queryset = CodexAgentDefinition.objects.all()
    serializer_class = AgentDefinitionSerializer
    filterset_fields = ["project", "category", "risk", "enabled"]


class ProtectedItemViewSet(BaseViewSet):
    queryset = ProtectedItem.objects.all()
    serializer_class = ProtectedItemSerializer
    filterset_fields = ["project", "item_type", "approved", "frozen"]

    def perform_update(self, serializer):
        if self.get_object().frozen:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Frozen ProtectedItem records cannot be modified through the generic ViewSet.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.frozen:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Frozen ProtectedItem records cannot be deleted.")
        instance.delete()


class WorkflowStepViewSet(BaseViewSet):
    queryset = CodexWorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    filterset_fields = ["project", "status"]


class LocalAIJobViewSet(ReadOnlyModelViewSet):
    queryset = LocalAIJob.objects.all()
    serializer_class = LocalAIJobSerializer
    permission_classes = [CodexAuthenticated]
    filterset_fields = ["project", "task_type", "status", "provider"]

class ProjectViewSet(ReadOnlyModelViewSet): queryset=ProjectRegistry.objects.all(); serializer_class=ProjectSerializer; permission_classes=[CodexAuthenticated]
class FeatureViewSet(BaseViewSet): queryset=Feature.objects.all(); serializer_class=FeatureSerializer; filterset_fields=["project","app_label","protected","status"]
class FileViewSet(ReadOnlyModelViewSet): queryset=FileRegistry.objects.all(); serializer_class=FileSerializer; permission_classes=[CodexAuthenticated]; filterset_fields=["project","kind","app_label","protected"]
class APIEndpointViewSet(ReadOnlyModelViewSet): queryset=APIEndpoint.objects.all(); serializer_class=APIEndpointSerializer; permission_classes=[CodexAuthenticated]; filterset_fields=["project","app_label","coverage_status","method"]
class ProtectedFeatureViewSet(BaseViewSet): queryset=ProtectedFeature.objects.all(); serializer_class=ProtectedFeatureSerializer; filterset_fields=["project","enabled"]
class ChangeSetViewSet(BaseViewSet):
    queryset=ChangeSet.objects.all()
    serializer_class=ChangeSetSerializer

class SnapshotViewSet(ReadOnlyModelViewSet): queryset=ProjectSnapshot.objects.all(); serializer_class=SnapshotSerializer; permission_classes=[CodexAuthenticated]

class OverviewView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self,request):
        project=ProjectRegistry.objects.get_or_create(key="so_iam_os",defaults={"name":"SO_IAM_OS"})[0]
        return Response({"project":ProjectSerializer(project).data,"counts":{"features":project.features.count(),"files":project.files.count(),"apis":project.apis.count(),"protected":project.protected_features.filter(enabled=True).count(),"changes":project.changesets.count(),"snapshots":project.snapshots.count()},"guarantee":"Every discovered backend API is represented in the frontend Codex API Registry at /codex."})

class ScanView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self,request):
        return Response(ProjectScanner().run())

class ContextView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self,request):
        project=ProjectRegistry.objects.get(key="so_iam_os"); return Response(ContextBuilder.build(project))

class PlanChangeView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self,request):
        obj=ChangePlanner.plan(user=request.user,title=request.data.get("title","Codex change plan"),objective=request.data.get("objective",""),paths=request.data.get("paths",[])); return Response(ChangeSetSerializer(obj).data, status=201)

class CreateSnapshotView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self,request):
        obj=SnapshotService.create(user=request.user,label=request.data.get("label","Codex snapshot")); return Response(SnapshotSerializer(obj).data,status=201)

import json

from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response

from .permissions import CodexAuthenticated
from .models import (
    ProjectRegistry,
    CodexConversation,
    CodexMessage,
    CodexAnalysis,
)
from .services.project_context import ProjectContextService
from .services.openai_service import OpenAIService


class OpenAICodexView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):

        message = str(
            request.data.get("message", "")
        ).strip()
        selected_paths = request.data.get("paths") or []
        if not isinstance(selected_paths, list):
            selected_paths = []

        if not message:
            return Response(
                {
                    "detail": "message is required."
                },
                status=400,
            )

        project = ProjectRegistry.objects.get(
            key="so_iam_os"
        )

        context = ProjectContextService(
            project=project
        ).build_context(message)
        # Multi-file Codex context: bounded, path-safe, read-only source payload.
        if selected_paths:
            root = Path(project.root_path or Path(settings.BASE_DIR).parent).resolve()
            selected_context = []
            total_chars = 0
            for rel in selected_paths[:20]:
                try:
                    target = (root / str(rel).replace("\\", "/")).resolve()
                    if root not in target.parents or not target.is_file():
                        continue
                    content = target.read_text(encoding="utf-8", errors="ignore")
                    remaining = max(0, 120_000 - total_chars)
                    content = content[:remaining]
                    selected_context.append({"path": target.relative_to(root).as_posix(), "content": content})
                    total_chars += len(content)
                    if total_chars >= 120_000:
                        break
                except (OSError, UnicodeError):
                    continue
            context["selected_files"] = selected_context

        conversation = CodexConversation.objects.create(
            project=project,
            user=request.user,
            title=message[:240],
            provider="openai",
        )

        CodexMessage.objects.create(
            conversation=conversation,
            role="user",
            content=message,
        )

        try:

            raw_result = OpenAIService().analyze(
                request=message,
                project_context=json.dumps(
                    context,
                    ensure_ascii=False,
                    indent=2,
                ),
                user=request.user,
            )

        except Exception as exc:

            return Response(
                {
                    "provider": "openai",
                    "success": False,
                    "detail": str(exc),
                },
                status=502,
            )

        result = self._parse_json(raw_result)

        CodexMessage.objects.create(
            conversation=conversation,
            role="assistant",
            content=raw_result,
        )

        analysis = CodexAnalysis.objects.create(
            conversation=conversation,
            request=message,
            provider="openai",
            result=result,
            context=context,
        )

        return Response(
            {
                "success": True,
                "provider": "openai",
                "conversation_id": conversation.id,
                "analysis_id": analysis.id,
                "context": context,
                "result": result,
                "raw": raw_result,
            }
        )

    @staticmethod
    def _parse_json(value):

        try:
            return json.loads(value)

        except (TypeError, json.JSONDecodeError):

            return {
                "type": "text",
                "content": value,
            }
# ---------------------------------------------------------------------------
# Codex V2 — project brain / safe agent / developer tools
# ---------------------------------------------------------------------------
from django.utils import timezone
from .models import ArchitectureNode, ArchitectureEdge, CodexPolicy, CodexTool, CodexAuditEvent, CodexFinding, CodexAgentRun, CodexExecutionRequest
from .services.intelligence import build_graph, search as project_search, impact as impact_analysis, security_scan, duplicate_scan, code_review, test_plan, agent_plan, ensure_policy, ensure_tools
from .services.execution import ALLOWED, run_safe

class IntelligenceBootstrapView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get_or_create(key='so_iam_os',defaults={'name':'SO_IAM_OS'})[0]
        ensure_tools(project); ensure_policy(project, request.user)
        graph=build_graph(project)
        findings=security_scan(project, request.user)
        return Response({'graph':graph,'security_findings':len(findings),'tools':CodexTool.objects.filter(project=project,enabled=True).count()})

class SearchView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'query':request.query_params.get('q',''),'results':project_search(project,request.query_params.get('q',''),int(request.query_params.get('limit',50)))})

class GraphView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        nodes=list(ArchitectureNode.objects.filter(project=project).values('id','key','kind','label','path','metadata'))
        edges=list(ArchitectureEdge.objects.filter(project=project).values('source_id','target_id','relation','metadata'))
        return Response({'nodes':nodes,'edges':edges})
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(build_graph(project))

class ImpactView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(impact_analysis(project,request.data.get('query','')))

class SecurityScanView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'findings':security_scan(project,request.user)})
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'findings':list(CodexFinding.objects.filter(project=project,category='security',resolved=False).values())})

class DuplicateScanView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'duplicates':duplicate_scan(project,request.user)})

class CodeReviewView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'path':request.data.get('path',''),'findings':code_review(project,request.data.get('path',''),request.user)})

class TestPlanView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(test_plan(project,request.data.get('target',''),request.user))

class AgentPlanView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        result=agent_plan(project,request.data.get('request',''),request.user)
        run=CodexAgentRun.objects.create(project=project,user=request.user,request=request.data.get('request',''),plan=result)
        result['run_id']=run.id
        return Response(result,status=201)

class PolicyView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'permissions':ensure_policy(project,request.user).permissions})
    def patch(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        policy=ensure_policy(project,request.user)
        permissions=dict(policy.permissions); permissions.update(request.data.get('permissions',{})); policy.permissions=permissions; policy.save(update_fields=['permissions','updated_at'])
        CodexAuditEvent.objects.create(project=project,user=request.user,event_type='policy',action='policy.update',payload={'permissions':permissions})
        return Response({'permissions':permissions})

class ToolsView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os'); ensure_tools(project)
        return Response(list(CodexTool.objects.filter(project=project).values()))

class AuditView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(list(CodexAuditEvent.objects.filter(project=project).order_by('-created_at')[:200].values()))

class SafeCommandsView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os'); policy=ensure_policy(project,request.user)
        return Response({'commands':[{'key':k,'command':v,'policy':policy.permissions.get('RUN_COMMANDS','DENY')} for k,v in ALLOWED.items()]})
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os'); key=request.data.get('key','')
        if request.data.get('confirm') is not True:
            return Response({'detail':'Explicit confirmation is required.','key':key},status=400)
        try:
            result=run_safe(request.user,project,key)
        except PermissionError as exc:
            CodexAuditEvent.objects.create(project=project,user=request.user,event_type='command',action=key,status='denied',payload={'reason':str(exc)})
            return Response({'detail':str(exc)},status=403)
        except Exception as exc:
            return Response({'detail':str(exc)},status=400)
        return Response(result)

class AgentRunView(APIView):
    permission_classes=[CodexAuthenticated]
    def get(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(list(CodexAgentRun.objects.filter(project=project).order_by('-created_at')[:100].values()))

class AutomationIntentView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        policy=ensure_policy(project,request.user)
        intent=request.data.get('intent','').strip()
        if not intent:
            return Response({'detail':'intent is required'},status=400)
        allowed=policy.permissions.get('AUTOMATION','DENY')
        plan={'intent':intent,'status':'planned','requires_approval':allowed!='ALLOW','policy':allowed,
              'actions':[{'action':'analyze_intent'},{'action':'resolve_automation_tool'},{'action':'request_approval' if allowed!='ALLOW' else 'execute'}],
              'guardrails':['Codex never executes arbitrary automation from natural language','Destructive actions require approval','All actions are audited']}
        CodexAuditEvent.objects.create(project=project,user=request.user,event_type='automation',action='automation.plan',payload=plan)
        return Response(plan,status=201)

from .services.intelligence import explain_feature, debug_error, generate_docs

class ExplainFeatureView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(explain_feature(project, request.data.get('query',''), request.user))

class DebugView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(debug_error(project, request.data.get('error',''), request.user))

class DocumentationView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        return Response(generate_docs(project, request.data.get('target',''), request.user))

from .services.execution import apply_changes, rollback_changes

class ApplyChangesView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        try:
            return Response(apply_changes(request.user,project,request.data.get('title','Codex change'),request.data.get('objective',''),request.data.get('changes',[]),request.data.get('confirm') is True),status=201)
        except PermissionError as exc:
            return Response({'detail':str(exc)},status=403)
        except Exception as exc:
            return Response({'detail':str(exc)},status=400)

class RollbackView(APIView):
    permission_classes=[CodexAuthenticated]
    def post(self, request, changeset_id):
        project=ProjectRegistry.objects.get(key='so_iam_os')
        try:
            return Response(rollback_changes(request.user,project,changeset_id,request.data.get('confirm') is True))
        except PermissionError as exc:
            return Response({'detail':str(exc)},status=403)
        except Exception as exc:
            return Response({'detail':str(exc)},status=400)

# ---------------------------------------------------------------------------
# Codex Capability Registry — 300 Features / 300 Tools / 300 Agents
# ---------------------------------------------------------------------------
from .models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition, CodexCapabilityRun, FileRegistry, ProtectedItem, CodexWorkflowStep, LocalAIJob
from .services.capabilities import ensure_capability_catalog, catalog_summary, execute_tool, execute_agent, health_report
from django.http import FileResponse
from django.db.models import Q
from pathlib import Path

class CapabilityRegistryMixin:
    permission_classes = [CodexAuthenticated]

    def project(self, *, create=False):
        if create:
            return ProjectRegistry.objects.get_or_create(key='so_iam_os', defaults={'name':'SO_IAM_OS'})[0]
        return ProjectRegistry.objects.filter(key='so_iam_os').first()

    def require_project(self):
        project = self.project()
        if project is None:
            from rest_framework.exceptions import NotFound
            raise NotFound('Codex project registry has not been bootstrapped yet.')
        return project

class CapabilityFeaturesView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project=self.require_project()
        qs=CodexFeatureDefinition.objects.filter(project=project, enabled=True)
        category=request.query_params.get('category')
        query=request.query_params.get('q','').strip()
        if category: qs=qs.filter(category=category)
        if query: qs=qs.filter(Q(name__icontains=query)|Q(key__icontains=query)|Q(purpose__icontains=query))
        return Response(list(qs.values()))

class CapabilityToolsView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project=self.require_project()
        qs=CodexToolDefinition.objects.filter(project=project, enabled=True)
        category=request.query_params.get('category'); query=request.query_params.get('q','').strip()
        if category: qs=qs.filter(category=category)
        if query: qs=qs.filter(Q(name__icontains=query)|Q(key__icontains=query)|Q(purpose__icontains=query))
        return Response(list(qs.values()))

class CapabilityAgentsView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project=self.require_project()
        qs=CodexAgentDefinition.objects.filter(project=project, enabled=True)
        category=request.query_params.get('category'); query=request.query_params.get('q','').strip()
        if category: qs=qs.filter(category=category)
        if query: qs=qs.filter(Q(name__icontains=query)|Q(key__icontains=query)|Q(purpose__icontains=query))
        return Response(list(qs.values()))

class CapabilitySummaryView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project=self.require_project()
        return Response(catalog_summary(project))

class CapabilityHealthView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        project=self.require_project()
        return Response(health_report(project))

class CapabilityBootstrapView(CapabilityRegistryMixin, APIView):
    def post(self, request):
        project=self.project(create=True); ensure_capability_catalog(project)
        return Response(catalog_summary(project), status=200)

class CapabilityValidateView(CapabilityRegistryMixin, APIView):
    def post(self, request):
        project=self.require_project()
        features=list(CodexFeatureDefinition.objects.filter(project=project,enabled=True).values('key'))
        tools=list(CodexToolDefinition.objects.filter(project=project,enabled=True).values('key'))
        agents=list(CodexAgentDefinition.objects.filter(project=project,enabled=True).values('key'))
        result={'features':len(features),'tools':len(tools),'agents':len(agents),'unique': all(len(x)==len({i['key'] for i in x}) for x in (features,tools,agents)), 'contracts': True}
        from .catalog import FEATURES, TOOLS, AGENTS
        result['expected']={'features':len(FEATURES),'tools':len(TOOLS),'agents':len(AGENTS)}
        result['passed']=all(result[k] == result['expected'][k] for k in ('features','tools','agents')) and result['unique']
        return Response(result, status=200 if result['passed'] else 500)

class CapabilityToolExecuteView(CapabilityRegistryMixin, APIView):
    def post(self, request, key):
        try:
            return Response(execute_tool(self.project(create=True), request.user, key, request.data or {}))
        except CodexToolDefinition.DoesNotExist:
            return Response({'detail':'Unknown or disabled Codex tool.'}, status=404)

class CapabilityAgentExecuteView(CapabilityRegistryMixin, APIView):
    def post(self, request, key):
        try:
            return Response(execute_agent(self.project(create=True), request.user, key, request.data or {}))
        except CodexAgentDefinition.DoesNotExist:
            return Response({'detail':'Unknown or disabled Codex agent.'}, status=404)

class CapabilityRunsView(CapabilityRegistryMixin, APIView):
    def get(self, request):
        qs=CodexCapabilityRun.objects.filter(project=self.require_project()).order_by('-created_at')[:200]
        return Response(list(qs.values()))

class ProjectContextExportView(CapabilityRegistryMixin, APIView):
    """Export repository context plus an explicitly bounded personal-work context."""
    def get(self, request):
        project = self.require_project()
        context = ContextBuilder.build(project)
        context['codex_capabilities'] = {
            'version': '1.0.0',
            'features': list(CodexFeatureDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'status', 'protection_level', 'permissions')),
            'tools': list(CodexToolDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'capability', 'risk', 'permission', 'input_schema', 'output_schema')),
            'agents': list(CodexAgentDefinition.objects.filter(project=project, enabled=True).values('key', 'name', 'category', 'purpose', 'tools', 'permissions', 'risk', 'validation')),
        }
        context['health'] = health_report(project)

        # Personal data is always scoped to request.user. Raw knowledge content is opt-in.
        include_personal = request.query_params.get('include_personal', 'true').lower() not in {'0', 'false', 'no'}
        if include_personal:
            from .services.user_context import build_user_context
            include_content = request.query_params.get('include_content', 'false').lower() in {'1', 'true', 'yes'}
            context['personal_context'] = build_user_context(
                request.user,
                limit=request.query_params.get('limit', 25),
                include_content=include_content,
            )
        else:
            context['personal_context'] = {
                'scope': 'omitted_by_request',
                'detail': 'Set include_personal=true to include the authenticated user’s Goals, Tasks, Knowledge, and Learning records.',
            }
        return Response(context)

class FileContentView(CapabilityRegistryMixin, APIView):
    def get(self, request, file_id):
        project=self.project()
        try: record=FileRegistry.objects.get(project=project,id=file_id)
        except FileRegistry.DoesNotExist: return Response({'detail':'File not found.'}, status=404)
        root=Path(project.root_path or Path(settings.BASE_DIR).parent).resolve(); target=(root/record.path).resolve()
        if root not in target.parents or not target.is_file():
            return Response({'detail':'File is outside the allowed project root or does not exist.'}, status=403)
        if target.stat().st_size > 2_000_000:
            return Response({'detail':'File is larger than the Codex viewer limit.', 'size':target.stat().st_size}, status=413)
        try: content=target.read_text(encoding='utf-8')
        except UnicodeDecodeError: return Response({'detail':'Binary file preview is not supported by the text viewer.'}, status=415)
        suffix=target.suffix.lower().lstrip('.') or 'text'
        return Response({'id':record.id,'path':record.path,'kind':record.kind,'size':target.stat().st_size,'language':suffix,'content':content})


# ---------------------------------------------------------------------------
# Codex governance / workflow / local AI / prompt / navigation extensions
# ---------------------------------------------------------------------------
from .services.extensions import (
    bootstrap_workflow, verify_workflow, freeze_item, generate_manifests,
    build_prompt, markdown_index, local_file_link, architecture_analyze,
    create_local_job,
)


class ProtectedRegistryView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        rows = list(ProtectedItem.objects.filter(project=project).values())
        return Response(rows)

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            item = freeze_item(project, request.user, request.data)
            return Response({"id": item.id, "key": item.key, "approved": item.approved, "frozen": item.frozen}, status=201)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)


class ProtectedManifestView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        return Response(generate_manifests(project))

    def post(self, request):
        return self.get(request)


class WorkflowView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        bootstrap_workflow(project)
        return Response(verify_workflow(project))

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        return Response(bootstrap_workflow(project))


class LocalAIJobsView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        qs = LocalAIJob.objects.filter(project=project).order_by("-created_at")[:100]
        return Response(list(qs.values()))

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        task_type = str(request.data.get("task_type", "metadata"))
        allowed = {x[0] for x in LocalAIJob.TASK_CHOICES}
        if task_type not in allowed:
            return Response({"detail": "Unsupported local AI task type."}, status=400)
        job = create_local_job(project, request.user, task_type, request.data.get("input_data") or {})
        return Response({"id": job.id, "status": job.status, "provider": job.provider}, status=202)


class LocalAIJobDetailView(APIView):
    permission_classes = [CodexAuthenticated]

    def get(self, request, job_id):
        try:
            job = LocalAIJob.objects.get(id=job_id)
        except LocalAIJob.DoesNotExist:
            return Response({"detail": "Local AI job not found."}, status=404)
        return Response({
            "id": job.id, "status": job.status, "task_type": job.task_type,
            "provider": job.provider, "result": job.result, "error": job.error,
            "created_at": job.created_at, "started_at": job.started_at, "completed_at": job.completed_at,
        })


class PromptGeneratorView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        prompt = build_prompt(project, request.data.get("prompt_type", "development"), request.data.get("goal", ""), request.data.get("paths") or [])
        return Response({"prompt": prompt, "copy_ready": True})


class MarkdownNavigationView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            return Response(markdown_index(project, request.data.get("path", "")))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)


class LocalFileOpenView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            return Response(local_file_link(project, request.data.get("path", "")))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)


class ArchitectureModuleAnalyzerView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        try:
            return Response(architecture_analyze(project, request.data.get("path", "")))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)


class SelectedFilesContextView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        root = Path(project.root_path or Path(settings.BASE_DIR).parent).resolve()
        paths = request.data.get("paths") or []
        if not isinstance(paths, list):
            return Response({"detail": "paths must be a list."}, status=400)
        rows, total = [], 0
        for rel in paths[:20]:
            try:
                target = (root / str(rel).replace("\\", "/")).resolve()
                if root not in target.parents or not target.is_file():
                    continue
                content = target.read_text(encoding="utf-8", errors="ignore")
                remaining = max(0, 120_000 - total)
                content = content[:remaining]
                rows.append({"path": target.relative_to(root).as_posix(), "content": content})
                total += len(content)
                if total >= 120_000:
                    break
            except (OSError, UnicodeError):
                continue
        return Response({"files": rows, "total_chars": total, "limit_chars": 120000})


class BuildWorkspaceView(APIView):
    """Read-only build graph generated from the actual project filesystem."""
    permission_classes = [CodexAuthenticated]

    def get(self, request):
        from .services.build_workspace import build_graph, root_for
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"}
        )[0]
        root = root_for(project)
        return Response({"project": project.name, "root_available": root.exists(),
                         "graph": build_graph(project),
                         "semantics": {"file_presence_is_not_execution": True,
                                        "read_only": True}})


class BuildManifestView(APIView):
    """Generate the versioned build manifest on explicit POST only."""
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        from .services.build_workspace import export_manifest
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"}
        )[0]
        return Response(export_manifest(project))
