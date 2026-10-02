from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import CodexAuthenticated
from .models import ProjectRegistry,Feature,FileRegistry,APIEndpoint,ProtectedFeature,ChangeSet,ProjectSnapshot
from .serializers import ProjectSerializer,FeatureSerializer,FileSerializer,APIEndpointSerializer,ProtectedFeatureSerializer,ChangeSetSerializer,SnapshotSerializer
from .services.project_scanner import ProjectScanner
from .services.context_builder import ContextBuilder
from .services.change_planner import ChangePlanner
from .services.snapshot_service import SnapshotService

class BaseViewSet(ModelViewSet): permission_classes=[CodexAuthenticated]
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
