from codex.models import ProtectedFeature
from codex.api.serializers import ProtectedFeatureSerializer
from codex.api.views.base_views import BaseViewSet


class ProtectedFeatureViewSet(BaseViewSet):
    queryset = ProtectedFeature.objects.all()
    serializer_class = ProtectedFeatureSerializer
    filterset_fields = ["project", "enabled"]
