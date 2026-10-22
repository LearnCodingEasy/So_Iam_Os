import uuid
from django.db import models
from django.conf import settings
from django.utils.timesince import timesince


class Website(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    base_url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    SOURCE_TYPES = [
        ("json", "JSON / REST API"),
        ("rss", "RSS / Atom"),
        ("html", "Public HTML"),
    ]
    source_type = models.CharField(max_length=12, choices=SOURCE_TYPES, default="html")
    config = models.JSONField(default=dict, blank=True, help_text="Connector settings; never store secrets here.")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="scraper_websites")
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(max_length=20, blank=True)
    last_error = models.TextField(blank=True)
    request_timeout = models.PositiveSmallIntegerField(default=15)

    class Meta:
        verbose_name = "Website"
        verbose_name_plural = "Websites"
        ordering = ['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)

    def __str__(self):
        return self.name


class ParentSelector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SELECTOR_TYPES = [
        ('css', 'CSS Selector'),
        ('xpath', 'XPath'),
    ]

    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name='parent_selectors')
    name = models.CharField(
        max_length=100, help_text="Example: Product Card or Job Item")
    selector = models.TextField(help_text="Example: .product-card")
    selector_type = models.CharField(
        max_length=10, choices=SELECTOR_TYPES, default='css')

    class Meta:
        verbose_name = "Parent Selector"
        verbose_name_plural = "Parent Selectors"
        ordering = ['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)

    def __str__(self):
        return f"{self.website.name} - {self.name}"


class ScrapingConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SELECTOR_TYPES = [
        ('css', 'CSS Selector'),
        ('xpath', 'XPath'),
    ]

    DATA_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('date', 'Date'),
        ('bool', 'Boolean'),
        ('html', 'Raw HTML'),
    ]

    parent = models.ForeignKey(
        ParentSelector, on_delete=models.CASCADE, related_name='child_fields')
    field_name = models.CharField(max_length=100)
    selector = models.TextField()
    selector_type = models.CharField(
        max_length=10, choices=SELECTOR_TYPES, default='css')
    extract_attr = models.CharField(
        max_length=100, null=True, blank=True, help_text="e.g., href, src")
    data_type = models.CharField(
        max_length=20, choices=DATA_TYPES, default='text')
    is_required = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Scraping Field"
        verbose_name_plural = "Scraping Fields"
        ordering = ['ordering']
        unique_together = ['parent', 'field_name']

    def __str__(self):
        return f"{self.parent.name} - {self.field_name}"


class ScrapingJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    target_url = models.URLField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    items_scraped = models.IntegerField(default=0)
    items_created = models.PositiveIntegerField(default=0)
    items_updated = models.PositiveIntegerField(default=0)
    items_duplicate = models.PositiveIntegerField(default=0)
    trigger_type = models.CharField(max_length=20, choices=[("manual", "Manual"), ("scheduled", "Scheduled")], default="manual")

    def __str__(self):
        return f"{self.website.name} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class ScrapedData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(
        ScrapingJob, on_delete=models.CASCADE, related_name='scraped_items')
    data = models.JSONField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField()

    def __str__(self):
        return f"Data from {self.job.website.name} - {self.scraped_at}"
