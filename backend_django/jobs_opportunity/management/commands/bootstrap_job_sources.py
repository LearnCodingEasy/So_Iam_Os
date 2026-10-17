from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs_opportunity.default_sources import DEFAULT_JOB_SOURCES
from jobs_opportunity.models import JobSource

class Command(BaseCommand):
    help = "Create opt-in development job-source presets for a user."
    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.get(email=options["email"])
        for preset in DEFAULT_JOB_SOURCES:
            config = {"adapter": preset["adapter"], "tos_confirmed": False, "robots_required": True, "notes": "Review source terms and configure board/site before enabling."}
            JobSource.objects.update_or_create(user=user, name=preset["name"], defaults={"source_type": preset["source_type"], "base_url": preset["base_url"], "enabled": False, "config": config})
        self.stdout.write(self.style.SUCCESS(f"Created/updated {len(DEFAULT_JOB_SOURCES)} opt-in source presets for {user.email}."))
