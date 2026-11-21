# notification security and testing

## Permission/ownership evidence

- notification/api/views/notification_views.py:L4: from rest_framework.permissions import IsAuthenticated
- notification/api/views/notification_views.py:L12: permission_classes = [IsAuthenticated]
- notification/api/views/notification_views.py:L15: def get_queryset(self):
- notification/api/views/notification_views.py:L16: qs = Notification.objects.filter(user=self.request.user, archived=False)
- notification/api/views/notification_views.py:L35: count = self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now())
- notification/api/views/notification_views.py:L40: return Response({"count": self.get_queryset().filter(read_at__isnull=True).count()})


## Tests
- notification/tests/test_notification.py
- notification/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
