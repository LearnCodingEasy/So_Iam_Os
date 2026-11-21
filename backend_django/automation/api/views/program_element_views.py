from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from automation.models import ProgramElement
from automation.api.serializers import ProgramElementSerializer


# ==================================================
# 2️⃣ ProgramElement
# ==================================================


class ProgramElementViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return ProgramElement.objects.filter(created_by=self.request.user)
    queryset = ProgramElement.objects.all()
    serializer_class = ProgramElementSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
