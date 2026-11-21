# notification API

Project prefix: /api/notifications/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: notification/api/urls.py

- L6: router.register("", NotificationViewSet, basename="notification")

## Handler declarations: notification/api/views/notification_views.py
L10: class NotificationViewSet(viewsets.ModelViewSet):
L11: serializer_class = NotificationSerializer
L12: permission_classes = [IsAuthenticated]
L15: def get_queryset(self):
L25: @action(detail=True, methods=["post"], url_path="read")
L33: @action(detail=False, methods=["post"], url_path="read-all")
L38: @action(detail=False, methods=["get"], url_path="unread-count")
L42: @action(detail=True, methods=["post"], url_path="archive")


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
