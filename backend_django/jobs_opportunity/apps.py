from django.apps import AppConfig


class JobsOpportunityConfig(AppConfig):
    name = 'jobs_opportunity'

    def ready(self):
        from . import signals  # noqa: F401
