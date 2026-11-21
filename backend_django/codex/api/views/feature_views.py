from codex.models import CodexFeatureDefinition
from codex.models import Feature, CodexFeatureDefinition
from codex.api.serializers import FeatureSerializer, FeatureDefinitionSerializer
from codex.api.views.base_views import BaseViewSet


class FeatureDefinitionViewSet(BaseViewSet):
    queryset = CodexFeatureDefinition.objects.all()
    serializer_class = FeatureDefinitionSerializer
    filterset_fields = ["project", "category", "status", "enabled"]


class FeatureViewSet(BaseViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filterset_fields = ["project", "app_label", "protected", "status"]
