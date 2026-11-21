import uuid
from django.db import models
from scraper.models.scraping_job import ScrapingJob


class ScrapedData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(
        ScrapingJob, on_delete=models.CASCADE, related_name='scraped_items')
    data = models.JSONField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField()

    def __str__(self):
        return f"Data from {self.job.website.name} - {self.scraped_at}"
