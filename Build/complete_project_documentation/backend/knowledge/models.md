# knowledge models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## knowledge_file
Source: knowledge/models/knowledge_file.py

- L10: class KnowledgeFile(models.Model):

- L21: class FileType(models.TextChoices):

- L48: file = models.FileField(

- L52: original_name = models.CharField(

- L60: file_type = models.CharField(

- L66: mime_type = models.CharField(

- L71: file_size = models.PositiveBigIntegerField(

- L79: description = models.TextField(

- L87: metadata = models.JSONField(

- L92: class ProcessingStatus(models.TextChoices):

- L98: processing_status = models.CharField(

- L103: processed_at = models.DateTimeField(null=True, blank=True)

- L104: processing_error = models.TextField(blank=True)

- L110: created_at = models.DateTimeField(

- L114: updated_at = models.DateTimeField(

- L122: class Meta:

- L127: indexes = [

- L128: models.Index(

- L136: models.Index(

## knowledge_item
Source: knowledge/models/knowledge_item.py

- L9: class KnowledgeItem(models.Model):

- L30: class KnowledgeType(models.TextChoices):

- L45: class Visibility(models.TextChoices):

- L63: title = models.CharField(

- L67: description = models.TextField(

- L71: content = models.TextField(

- L79: knowledge_type = models.CharField(

- L89: source_url = models.URLField(

- L93: source_name = models.CharField(

- L102: tags = models.JSONField(

- L111: metadata = models.JSONField(

- L120: visibility = models.CharField(

- L130: is_archived = models.BooleanField(

- L138: created_at = models.DateTimeField(

- L142: updated_at = models.DateTimeField(

- L150: class Meta:

- L155: indexes = [

- L156: models.Index(

- L164: models.Index(

- L172: models.Index(

- L180: models.Index(

## __init__
Source: knowledge/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
