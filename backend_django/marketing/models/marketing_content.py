from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class MarketingContent(models.Model):
    """A piece of promotional content, optionally tied to a campaign."""

    TYPE_CHOICES = [('post', 'Post'), ('article', 'Article'), ('email', 'Email'), ('video', 'Video'), ('landing_page', 'Landing page'), ('other', 'Other')]
    STATUS_CHOICES = [('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published')]
    TYPE_POST = 'post'
    TYPE_ARTICLE = 'article'
    TYPE_EMAIL = 'email'
    TYPE_VIDEO = 'video'
    TYPE_LANDING_PAGE = 'landing_page'
    TYPE_OTHER = 'other'
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_PUBLISHED = 'published'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_content')
    campaign = models.ForeignKey('marketing.Campaign', null=True, blank=True, on_delete=models.SET_NULL, related_name='contents')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='post')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    publish_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.title)
