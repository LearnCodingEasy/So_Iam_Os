# Hand-written initial migration (Django was not available to run makemigrations).
# Field definitions mirror the models exactly; verify with
#   python manage.py makemigrations --check --dry-run

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='agents')),
                ('name', models.CharField(max_length=160)),
                ('role', models.CharField(max_length=160, blank=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('paused', 'Paused'), ('archived', 'Archived')], default='draft')),
                ('model_name', models.CharField(max_length=120, blank=True)),
                ('system_prompt', models.TextField(blank=True)),
                ('requires_approval', models.BooleanField(default=True)),
                ('metadata', models.JSONField(default=dict, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='AgentConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey('agents.agent', on_delete=django.db.models.deletion.CASCADE, related_name='configurations')),
                ('version', models.PositiveIntegerField(default=1)),
                ('temperature', models.FloatField(default=0.2)),
                ('max_steps', models.PositiveIntegerField(default=10)),
                ('tools', models.JSONField(default=list, blank=True)),
                ('parameters', models.JSONField(default=dict, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-version'], 'constraints': [models.UniqueConstraint(fields=['agent', 'version'], name='agent_configuration_version_unique')]},
        ),
        migrations.CreateModel(
            name='AgentRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='agent_runs')),
                ('agent', models.ForeignKey('agents.agent', on_delete=django.db.models.deletion.CASCADE, related_name='runs')),
                ('configuration', models.ForeignKey('agents.agentconfiguration', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runs')),
                ('goal', models.TextField()),
                ('status', models.CharField(max_length=20, choices=[('pending', 'Pending'), ('awaiting_approval', 'Awaiting approval'), ('running', 'Running'), ('succeeded', 'Succeeded'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending')),
                ('input_data', models.JSONField(default=dict, blank=True)),
                ('result', models.JSONField(default=dict, blank=True)),
                ('error', models.TextField(blank=True)),
                ('approved_at', models.DateTimeField(null=True, blank=True)),
                ('started_at', models.DateTimeField(null=True, blank=True)),
                ('finished_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='AgentExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.ForeignKey('agents.agentrun', on_delete=django.db.models.deletion.CASCADE, related_name='executions')),
                ('step_index', models.PositiveIntegerField(default=0)),
                ('action', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=20, choices=[('pending', 'Pending'), ('running', 'Running'), ('succeeded', 'Succeeded'), ('failed', 'Failed'), ('skipped', 'Skipped')], default='pending')),
                ('input_data', models.JSONField(default=dict, blank=True)),
                ('output_data', models.JSONField(default=dict, blank=True)),
                ('error', models.TextField(blank=True)),
                ('duration_ms', models.PositiveIntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['step_index', 'id']},
        ),
    ]
