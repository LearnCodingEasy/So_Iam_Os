from codex.models import ProtectedItem
from codex.models import ProtectedItem
from codex.api.serializers import ProtectedItemSerializer
from codex.api.views.base_views import BaseViewSet


class ProtectedItemViewSet(BaseViewSet):
    queryset = ProtectedItem.objects.all()
    serializer_class = ProtectedItemSerializer
    filterset_fields = ["project", "item_type", "approved", "frozen"]

    def perform_update(self, serializer):
        if self.get_object().frozen:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Frozen ProtectedItem records cannot be modified through the generic ViewSet.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.frozen:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Frozen ProtectedItem records cannot be deleted.")
        instance.delete()
