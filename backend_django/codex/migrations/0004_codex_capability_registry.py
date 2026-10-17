from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('codex', '0003_codex_intelligence')]

    operations = [
        migrations.CreateModel(
            name='CodexFeatureDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=180)), ('name', models.CharField(max_length=220)),
                ('category', models.CharField(max_length=120)), ('purpose', models.TextField(blank=True)),
                ('status', models.CharField(default='implemented', max_length=30)),
                ('protection_level', models.CharField(default='NORMAL', max_length=30)),
                ('permissions', models.JSONField(blank=True, default=list)), ('integration', models.JSONField(blank=True, default=dict)),
                ('tests', models.JSONField(blank=True, default=list)), ('metadata', models.JSONField(blank=True, default=dict)),
                ('enabled', models.BooleanField(default=True)), ('version', models.CharField(default='1.0.0', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_definitions', to='codex.projectregistry')),
            ], options={'ordering': ['category', 'id']},
        ),
        migrations.CreateModel(
            name='CodexToolDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=180)), ('name', models.CharField(max_length=220)),
                ('category', models.CharField(max_length=120)), ('capability', models.CharField(default='read', max_length=40)),
                ('risk', models.CharField(default='low', max_length=30)), ('permission', models.CharField(default='READ_FILES', max_length=80)),
                ('input_schema', models.JSONField(blank=True, default=dict)), ('output_schema', models.JSONField(blank=True, default=dict)),
                ('purpose', models.TextField(blank=True)), ('implementation', models.CharField(default='catalog_dispatch', max_length=120)),
                ('enabled', models.BooleanField(default=True)), ('version', models.CharField(default='1.0.0', max_length=30)),
                ('metadata', models.JSONField(blank=True, default=dict)), ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tool_definitions', to='codex.projectregistry')),
            ], options={'ordering': ['category', 'id']},
        ),
        migrations.CreateModel(
            name='CodexAgentDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=180)), ('name', models.CharField(max_length=220)),
                ('category', models.CharField(max_length=120)), ('purpose', models.TextField(blank=True)),
                ('input_schema', models.JSONField(blank=True, default=dict)), ('output_schema', models.JSONField(blank=True, default=dict)),
                ('tools', models.JSONField(blank=True, default=list)), ('permissions', models.JSONField(blank=True, default=list)),
                ('risk', models.CharField(default='medium', max_length=30)), ('validation', models.JSONField(blank=True, default=list)),
                ('implementation', models.CharField(default='catalog_orchestrator', max_length=120)),
                ('enabled', models.BooleanField(default=True)), ('version', models.CharField(default='1.0.0', max_length=30)),
                ('metadata', models.JSONField(blank=True, default=dict)), ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_definitions', to='codex.projectregistry')),
            ], options={'ordering': ['category', 'id']},
        ),
        migrations.CreateModel(
            name='CodexCapabilityRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('tool','Tool'),('agent','Agent'),('feature','Feature')], max_length=20)),
                ('key', models.CharField(max_length=180)),
                ('status', models.CharField(choices=[('planned','Planned'),('completed','Completed'),('failed','Failed'),('denied','Denied')], default='planned', max_length=30)),
                ('input_data', models.JSONField(blank=True, default=dict)), ('output_data', models.JSONField(blank=True, default=dict)),
                ('validation', models.JSONField(blank=True, default=dict)), ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capability_runs', to='codex.projectregistry')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(model_name='codexfeaturedefinition', constraint=models.UniqueConstraint(fields=('project','key'), name='codex_feature_definition_project_key_unique')),
        migrations.AddConstraint(model_name='codextooldefinition', constraint=models.UniqueConstraint(fields=('project','key'), name='codex_tool_definition_project_key_unique')),
        migrations.AddConstraint(model_name='codexagentdefinition', constraint=models.UniqueConstraint(fields=('project','key'), name='codex_agent_definition_project_key_unique')),
    ]
