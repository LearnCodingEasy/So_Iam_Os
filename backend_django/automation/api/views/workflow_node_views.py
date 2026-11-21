from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import WorkflowNode
from automation.api.serializers import WorkflowNodeSerializer, ActionSerializer
from automation.engine_runtime import run_action_instance


# ==================================================
# 4️⃣ WorkflowNode (VueFlow Node)
# ==================================================


class WorkflowNodeViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return WorkflowNode.objects.filter(created_by=self.request.user)
    queryset = WorkflowNode.objects.all()
    serializer_class = WorkflowNodeSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        """
        ▶️ تشغيل Node واحدة فقط (Debug / Test)
        """
        node = self.get_object()
        results = []

        # جلب كل الـ Actions المرتبطة بالنود
        actions = node.actions.all().order_by("created_at")

        for action_obj in actions:
            result = run_action_instance(
                action_obj,
                node.program
            )
            results.append({
                "action_id": action_obj.id,
                "result": result
            })

        return Response({
            "status": "node_executed",
            "node_id": node.id,
            "results": results
        })

    """
    🔗 جلب كل الأحداث المرتبطة بـ Node محدد
    """

    @action(detail=True, methods=["get"])
    def full_events(self, request, pk=None):
        node = self.get_object()

        # =========================
        # 1️⃣ actions
        # =========================
        actions = node.actions.all().order_by("created_at")

        return Response({
            "node": WorkflowNodeSerializer(node).data,
            "actions": ActionSerializer(actions, many=True).data,
        })
