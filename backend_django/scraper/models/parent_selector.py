import uuid
from django.db import models
from django.utils.timesince import timesince
from scraper.models.website import Website


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
