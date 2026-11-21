from rest_framework.viewsets import ReadOnlyModelViewSet
from codex.permissions import CodexAuthenticated
from codex.models import APIEndpoint
from codex.api.serializers import APIEndpointSerializer


class APIEndpointViewSet(ReadOnlyModelViewSet):
    queryset = APIEndpoint.objects.all()
    serializer_class = APIEndpointSerializer
    permission_classes = [CodexAuthenticated]
    filterset_fields = ["project", "app_label", "coverage_status", "method"]
