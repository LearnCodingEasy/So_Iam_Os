from django.core.management.base import BaseCommand
from codex.services.project_scanner import ProjectScanner
class Command(BaseCommand):
    help="Scan SO_IAM_OS files, features and backend APIs into Codex registries."
    def handle(self,*args,**kwargs): self.stdout.write(str(ProjectScanner().run()))
