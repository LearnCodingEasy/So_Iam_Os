from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import Delay
from automation.api.serializers import DelaySerializer


# ==================================================
# 🔟 Delay
# ==================================================


class DelayViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self): return Delay.objects.filter(created_by=self.request.user)
    queryset = Delay.objects.all()
    serializer_class = DelaySerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # Send Created By user Created Program

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
