from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import ScreenState
from automation.api.serializers import ScreenStateSerializer


# ==================================================
# 9️⃣ ScreenState
# ==================================================
class ScreenStateViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return ScreenState.objects.filter(created_by=self.request.user)
    """
    🎥 ScreenState API
    ------------------
    مسؤول عن:
    - حفظ لحظات التركيز أثناء الفيديو
    - تحديد zoom / highlight / arrows
    - ربط الأحداث بزمن الفيديو
    """

    queryset = ScreenState.objects.all()
    # queryset = ScreenState.objects.all().order_by("start_time")
    serializer_class = ScreenStateSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """
        📦 Bulk Create
        -------------
        استقبال مجموعة ScreenStates مرة واحدة
        (مفيد عند استيراد JSON من الأوتوميشن)
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"status": "screen_states_created", "count": len(serializer.data)},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["get"])
    def by_task_run(self, request):
        """
        🔗 Filter by TaskRun
        -------------------
        جلب كل ScreenStates الخاصة بتسجيل معين
        """
        task_run_id = request.query_params.get("task_run")
        if not task_run_id:
            return Response(
                {"error": "task_run parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        states = ScreenState.objects.filter(task_run_id=task_run_id)
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)
