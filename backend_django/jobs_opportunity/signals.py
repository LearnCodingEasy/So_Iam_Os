from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .default_sources import DEFAULT_JOB_SOURCES
from .models import JobSource

@receiver(post_save, sender=get_user_model())
def provision_default_job_sources(sender, instance, created, **kwargs):
    if not created:
        return
    for preset in DEFAULT_JOB_SOURCES:
        JobSource.objects.get_or_create(user=instance, name=preset['name'], defaults={
            'source_type': preset['source_type'], 'base_url': preset['base_url'], 'enabled': False,
            'config': {'adapter': preset['adapter'], 'terms_confirmed': False, 'robots_required': True,
                       'notes': 'Review source terms and configure board/site before enabling.'},
        })
