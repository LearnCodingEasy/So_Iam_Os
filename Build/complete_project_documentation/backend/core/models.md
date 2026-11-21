# core models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## base_model
Source: core/models/base_model.py

- L5: class BaseModel(models.Model):

- L6: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L7: created_at = models.DateTimeField(auto_now_add=True, db_index=True)

- L8: updated_at = models.DateTimeField(auto_now=True)

- L9: class Meta:

## user_learning_settings
Source: core/models/user_learning_settings.py

- L5: class UserLearningSettings(models.Model):

- L6: user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_settings")

- L7: daily_learning_tasks = models.PositiveSmallIntegerField(default=5)

- L11: task_generation_enabled = models.BooleanField(default=True)

- L12: preferred_learning_time = models.TimeField(null=True, blank=True)

- L13: updated_at = models.DateTimeField(auto_now=True)

- L15: class Meta:

- L16: constraints = [models.CheckConstraint(condition=models.Q(daily_learning_tasks__gte=1) & models.Q(daily_learning_tasks__lte=10), name="learning_tasks_1_10")]

## __init__
Source: core/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
