# scraper models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## parent_selector
Source: scraper/models/parent_selector.py

- L7: class ParentSelector(models.Model):

- L8: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L9: created_at = models.DateTimeField(auto_now_add=True)

- L10: updated_at = models.DateTimeField(auto_now=True)

- L19: name = models.CharField(

- L21: selector = models.TextField(help_text="Example: .product-card")

- L22: selector_type = models.CharField(

- L25: class Meta:

## scraped_data
Source: scraper/models/scraped_data.py

- L6: class ScrapedData(models.Model):

- L7: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L10: data = models.JSONField()

- L11: scraped_at = models.DateTimeField(auto_now_add=True)

- L12: source_url = models.URLField()

## scraping_config
Source: scraper/models/scraping_config.py

- L6: class ScrapingConfig(models.Model):

- L7: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L8: created_at = models.DateTimeField(auto_now_add=True)

- L9: updated_at = models.DateTimeField(auto_now=True)

- L28: field_name = models.CharField(max_length=100)

- L29: selector = models.TextField()

- L30: selector_type = models.CharField(

- L32: extract_attr = models.CharField(

- L34: data_type = models.CharField(

- L36: is_required = models.BooleanField(default=True)

- L37: ordering = models.PositiveIntegerField(default=0)

- L38: notes = models.TextField(blank=True, null=True)

- L40: class Meta:

## scraping_job
Source: scraper/models/scraping_job.py

- L6: class ScrapingJob(models.Model):

- L7: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L16: target_url = models.URLField()

- L17: status = models.CharField(

- L19: started_at = models.DateTimeField(auto_now_add=True)

- L20: completed_at = models.DateTimeField(null=True, blank=True)

- L21: error_message = models.TextField(blank=True)

- L22: items_scraped = models.IntegerField(default=0)

- L23: items_created = models.PositiveIntegerField(default=0)

- L24: items_updated = models.PositiveIntegerField(default=0)

- L25: items_duplicate = models.PositiveIntegerField(default=0)

- L26: trigger_type = models.CharField(max_length=20, choices=[("manual", "Manual"), ("scheduled", "Scheduled")], default="manual")

## website
Source: scraper/models/website.py

- L7: class Website(models.Model):

- L8: id = models.UUIDField(

- L10: created_at = models.DateTimeField(auto_now_add=True)

- L11: updated_at = models.DateTimeField(auto_now=True)

- L13: name = models.CharField(max_length=200)

- L14: base_url = models.URLField()

- L15: description = models.TextField(blank=True)

- L16: is_active = models.BooleanField(default=True)

- L22: source_type = models.CharField(max_length=12, choices=SOURCE_TYPES, default="html")

- L23: config = models.JSONField(default=dict, blank=True, help_text="Connector settings; never store secrets here.")

- L25: last_run_at = models.DateTimeField(null=True, blank=True)

- L26: last_status = models.CharField(max_length=20, blank=True)

- L27: last_error = models.TextField(blank=True)

- L28: request_timeout = models.PositiveSmallIntegerField(default=15)

- L30: class Meta:

## __init__
Source: scraper/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
