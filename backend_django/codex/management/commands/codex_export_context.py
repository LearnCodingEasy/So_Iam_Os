import json
from pathlib import Path
from django.core.management.base import BaseCommand
from codex.models import ProjectRegistry
from codex.services.capabilities import ensure_capability_catalog, health_report
from codex.services.context_builder import ContextBuilder
from codex.models import CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition

class Command(BaseCommand):
    help = 'Export the live Codex project contract to project-context/codex-project-context.json.'
    def handle(self, *args, **options):
        project=ProjectRegistry.objects.get_or_create(key='so_iam_os', defaults={'name':'SO_IAM_OS'})[0]
        ensure_capability_catalog(project)
        context=ContextBuilder.build(project)
        context['schema_version']='1.0.0'
        context['codex_capabilities']={
            'features':list(CodexFeatureDefinition.objects.filter(project=project,enabled=True).values()),
            'tools':list(CodexToolDefinition.objects.filter(project=project,enabled=True).values()),
            'agents':list(CodexAgentDefinition.objects.filter(project=project,enabled=True).values()),
        }
        context['health']=health_report(project)
        path=Path(__file__).resolve().parents[4] / 'project-context' / 'codex-project-context.json'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(context,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Exported {path}'))
