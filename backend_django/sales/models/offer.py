from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Offer(models.Model):
    """Something the user sells (service, product, package)."""

    STATUS_CHOICES = [('draft', 'Draft'), ('active', 'Active'), ('retired', 'Retired')]
    STATUS_DRAFT = 'draft'
    STATUS_ACTIVE = 'active'
    STATUS_RETIRED = 'retired'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_offers')
    project = models.ForeignKey('projects.Project', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales_offers')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
