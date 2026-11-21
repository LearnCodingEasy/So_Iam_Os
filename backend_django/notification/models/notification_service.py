from django.contrib.contenttypes.models import ContentType
from notification.models.notification import Notification


class NotificationService:
    @staticmethod
    def create(user, *, type=Notification.Type.SYSTEM, title, message, action_url="", priority=50, obj=None, metadata=None):
        kwargs = dict(user=user, type=type, title=title, message=message, action_url=action_url, priority=priority, metadata=metadata or {})
        if obj is not None:
            kwargs["content_type"] = ContentType.objects.get_for_model(obj.__class__)
            kwargs["object_id"] = str(obj.pk)
        return Notification.objects.create(**kwargs)
