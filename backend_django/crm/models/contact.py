from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Contact(models.Model):
    """A person the user has a (potential) business relationship with. Owner of contact data."""

    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')]
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_ARCHIVED = 'archived'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crm_contacts')
    company = models.ForeignKey('crm.Company', null=True, blank=True, on_delete=models.SET_NULL, related_name='contacts')
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    job_title = models.CharField(max_length=160, blank=True)
    source = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return str(self.full_name)

    @property
    def full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()
