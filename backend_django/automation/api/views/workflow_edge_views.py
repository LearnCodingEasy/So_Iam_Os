from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import WorkflowEdge
from automation.api.serializers import WorkflowEdgeSerializer


# ==================================================
# 5️⃣ WorkflowEdge
# ==================================================


class WorkflowEdgeViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return WorkflowEdge.objects.filter(created_by=self.request.user)
    queryset = WorkflowEdge.objects.all()
    serializer_class = WorkflowEdgeSerializer

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user
                        )
