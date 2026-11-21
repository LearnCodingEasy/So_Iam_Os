from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import TaskRun
from automation.api.serializers import TaskRunSerializer


# ==================================================
# 8️⃣ TaskRun
# ==================================================

class TaskRunViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return TaskRun.objects.filter(created_by=self.request.user)
    queryset = TaskRun.objects.all().order_by("-started_at")
    serializer_class = TaskRunSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
