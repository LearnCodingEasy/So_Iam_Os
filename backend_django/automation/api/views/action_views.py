from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import Action
from automation.api.serializers import ActionSerializer
from automation.engine_runtime import run_action_instance
from django.db.models import Count


# ==================================================
# 6️⃣ Action
# ==================================================

class ActionViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return Action.objects.filter(created_by=self.request.user)
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # Send Created By user Created Program
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # 🔹 تعديل الأكشن
    @action(detail=True, methods=['patch'])
    def update_type(self, request, pk=None):
        action_obj = self.get_object()
        new_type = request.data.get("action_type")
        if new_type:
            action_obj.action_type = new_type
            action_obj.save()
            return Response({"success": True, "action_type": action_obj.action_type})
        return Response({"success": False, "error": "No action_type provided"}, status=400)

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        action = self.get_object()
        result = run_action_instance(
            action,
            action.node.program if action.node else None
        )
        return Response(result)

    # ============================================
    # 🧠 Templates by Program
    # ============================================
    @action(detail=False, methods=["get"])
    def templates_by_program(self, request):
        program_id = request.query_params.get("program")

        if not program_id:
            return Response({"error": "program required"}, status=400)

        actions = (
            Action.objects
            .filter(node__program_id=program_id)
            .values("action_type", "payload")
            .annotate(usage_count=Count("id"))
            .order_by("-usage_count")
        )

        return Response(actions)
