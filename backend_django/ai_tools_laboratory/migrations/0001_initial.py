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
            name='ToolCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='ai_tool_categories')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name'], 'constraints': [models.UniqueConstraint(fields=['user', 'name'], name='ai_tool_category_user_name_unique')]},
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='ai_tools')),
                ('category', models.ForeignKey('ai_tools_laboratory.toolcategory', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tools')),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('vendor', models.CharField(max_length=160, blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('evaluating', 'Evaluating'), ('adopted', 'Adopted'), ('rejected', 'Rejected'), ('archived', 'Archived')], default='evaluating')),
                ('rating', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('pricing_model', models.CharField(max_length=80, blank=True)),
                ('tags', models.JSONField(default=list, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='ToolConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool', models.ForeignKey('ai_tools_laboratory.tool', on_delete=django.db.models.deletion.CASCADE, related_name='configurations')),
                ('name', models.CharField(max_length=120)),
                ('settings', models.JSONField(default=dict, blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-is_default', 'name']},
        ),
        migrations.CreateModel(
            name='ToolExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='ai_tool_executions')),
                ('tool', models.ForeignKey('ai_tools_laboratory.tool', on_delete=django.db.models.deletion.CASCADE, related_name='executions')),
                ('configuration', models.ForeignKey('ai_tools_laboratory.toolconfiguration', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executions')),
                ('input_text', models.TextField(blank=True)),
                ('output_text', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('pending', 'Pending'), ('succeeded', 'Succeeded'), ('failed', 'Failed')], default='pending')),
                ('notes', models.TextField(blank=True)),
                ('duration_ms', models.PositiveIntegerField(null=True, blank=True)),
                ('executed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-executed_at']},
        ),
    ]
