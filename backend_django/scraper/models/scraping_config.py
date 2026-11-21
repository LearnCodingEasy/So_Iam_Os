import uuid
from django.db import models
from scraper.models.parent_selector import ParentSelector


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
