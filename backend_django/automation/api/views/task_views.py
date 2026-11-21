from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import Task
from automation.api.serializers import TaskSerializer


# ==================================================
# 7️⃣ Task
# ==================================================


class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return Task.objects.filter(created_by=self.request.user)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
