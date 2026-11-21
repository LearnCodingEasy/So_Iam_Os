import uuid
from django.db import models
from scraper.models.website import Website


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
