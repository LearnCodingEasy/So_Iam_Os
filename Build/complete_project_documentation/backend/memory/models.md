# memory models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## memory_item
Source: memory/models/memory_item.py

- L5: class MemoryItem(models.Model):

- L6: class Type(models.TextChoices):

- L9: type=models.CharField(max_length=30,choices=Type.choices,default=Type.FACT)

- L10: key=models.CharField(max_length=200)

- L11: content=models.TextField()

- L12: source=models.CharField(max_length=100,blank=True)

- L13: importance=models.PositiveSmallIntegerField(default=50)

- L14: is_active=models.BooleanField(default=True)

- L15: metadata=models.JSONField(default=dict,blank=True)

- L16: created_at=models.DateTimeField(auto_now_add=True)

- L17: updated_at=models.DateTimeField(auto_now=True)

- L18: class Meta:

- L20: indexes=[models.Index(fields=['user','type','is_active']),models.Index(fields=['user','key'])]

## __init__
Source: memory/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
