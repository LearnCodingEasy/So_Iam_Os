# notification models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## notification
Source: notification/models/notification.py

- L8: class Notification(models.Model):

- L9: class Type(models.TextChoices):

- L20: type = models.CharField(max_length=30, choices=Type.choices, default=Type.SYSTEM)

- L21: title = models.CharField(max_length=255)

- L22: message = models.TextField()

- L23: action_url = models.CharField(max_length=500, blank=True)

- L24: priority = models.PositiveSmallIntegerField(default=50)

- L25: read_at = models.DateTimeField(null=True, blank=True)

- L26: archived = models.BooleanField(default=False)

- L28: object_id = models.CharField(max_length=255, blank=True)

- L30: metadata = models.JSONField(default=dict, blank=True)

- L31: created_at = models.DateTimeField(auto_now_add=True)

- L33: class Meta:

- L35: indexes = [

- L36: models.Index(fields=["user", "read_at", "created_at"]),

- L37: models.Index(fields=["user", "type", "created_at"]),

## notification_service
Source: notification/models/notification_service.py

- L5: class NotificationService:

## __init__
Source: notification/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
