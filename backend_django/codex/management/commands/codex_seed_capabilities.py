from django.core.management.base import BaseCommand
from codex.models import ProjectRegistry
from codex.services.capabilities import ensure_capability_catalog, catalog_summary

class Command(BaseCommand):
    help = 'Seed and validate the canonical 300-feature / 300-tool / 300-agent Codex registry.'
    def handle(self, *args, **options):
        project = ProjectRegistry.objects.get_or_create(key='so_iam_os', defaults={'name':'SO_IAM_OS'})[0]
        ensure_capability_catalog(project)
        self.stdout.write(self.style.SUCCESS(str(catalog_summary(project))))
