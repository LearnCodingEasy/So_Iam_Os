# tasks models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## task
Source: tasks/models/task.py

- L6: class Task(models.Model):

- L7: class Status(models.TextChoices):

- L14: class Priority(models.TextChoices):

- L35: title = models.CharField(max_length=255)

- L36: description = models.TextField(blank=True)

- L37: scheduled_date = models.DateField(default=timezone.localdate)

- L38: scheduled_start = models.TimeField(null=True, blank=True)

- L39: due_at = models.DateTimeField(null=True, blank=True)

- L40: estimated_minutes = models.PositiveIntegerField(default=0)

- L41: actual_minutes = models.PositiveIntegerField(default=0)

- L42: priority = models.CharField(

- L44: status = models.CharField(

- L46: sort_order = models.PositiveIntegerField(default=0)

- L47: completed_at = models.DateTimeField(null=True, blank=True)

- L48: postponed_until = models.DateField(null=True, blank=True)

- L49: recurrence_rule = models.JSONField(default=dict, blank=True)

- L50: metadata = models.JSONField(default=dict, blank=True)

- L51: created_at = models.DateTimeField(auto_now_add=True)

- L52: updated_at = models.DateTimeField(auto_now=True)

- L54: class Meta:

- L57: indexes = [

- L58: models.Index(fields=["user", "scheduled_date", "status"]),

- L59: models.Index(fields=["user", "priority"]),

- L60: models.Index(fields=["goal", "status"]),

- L61: models.Index(fields=["learning_topic", "status"]),

## __init__
Source: tasks/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
