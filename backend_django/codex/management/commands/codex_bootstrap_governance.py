from django.core.management.base import BaseCommand
from codex.models import ProjectRegistry
from codex.services.extensions import bootstrap_workflow, generate_manifests


class Command(BaseCommand):
    help = "Bootstrap Codex workflow and governance manifests."

    def handle(self, *args, **options):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"}
        )[0]
        workflow = bootstrap_workflow(project)
        manifest = generate_manifests(project)
        self.stdout.write(self.style.SUCCESS(
            f"Codex governance ready: workflow={workflow['completed']}/{workflow['total']} "
            f"protected={manifest['protected_count']}"
        ))
