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