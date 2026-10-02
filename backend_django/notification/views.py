from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user, archived=False)
        kind = self.request.query_params.get("type")
        unread = self.request.query_params.get("unread")
        if kind:
            qs = qs.filter(type=kind)
        if unread in {"1", "true", "True"}:
            qs = qs.filter(read_at__isnull=True)
        return qs

    @action(detail=True, methods=["post"], url_path="read")
    def read(self, request, pk=None):
        item = self.get_object()
        if not item.read_at:
            item.read_at = timezone.now()
            item.save(update_fields=["read_at"])
        return Response(self.get_serializer(item).data)

    @action(detail=False, methods=["post"], url_path="read-all")
    def read_all(self, request):
        count = self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now())
        return Response({"updated": count})

    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        return Response({"count": self.get_queryset().filter(read_at__isnull=True).count()})

    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, pk=None):
        item = self.get_object()
        item.archived = True
        item.save(update_fields=["archived"])
        return Response(status=status.HTTP_204_NO_CONTENT)
