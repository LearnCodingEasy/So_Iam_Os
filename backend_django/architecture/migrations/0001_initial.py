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
            name='Architecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='architectures')),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('deprecated', 'Deprecated')], default='draft')),
                ('version', models.CharField(max_length=40, default='1.0')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('architecture', models.ForeignKey('architecture.architecture', on_delete=django.db.models.deletion.CASCADE, related_name='components')),
                ('name', models.CharField(max_length=160)),
                ('component_type', models.CharField(max_length=20, choices=[('service', 'Service'), ('database', 'Database'), ('queue', 'Queue'), ('frontend', 'Frontend'), ('library', 'Library'), ('external', 'External'), ('other', 'Other')], default='service')),
                ('description', models.TextField(blank=True)),
                ('technology', models.CharField(max_length=160, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name'], 'constraints': [models.UniqueConstraint(fields=['architecture', 'name'], name='architecture_component_name_unique')]},
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.ForeignKey('architecture.component', on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_dependencies')),
                ('target', models.ForeignKey('architecture.component', on_delete=django.db.models.deletion.CASCADE, related_name='incoming_dependencies')),
                ('dependency_type', models.CharField(max_length=20, choices=[('depends_on', 'Depends on'), ('calls', 'Calls'), ('reads', 'Reads from'), ('writes', 'Writes to')], default='depends_on')),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['id'], 'constraints': [models.UniqueConstraint(fields=['source', 'target', 'dependency_type'], name='architecture_dependency_unique')]},
        ),
        migrations.CreateModel(
            name='ArchitectureDecision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('architecture', models.ForeignKey('architecture.architecture', on_delete=django.db.models.deletion.CASCADE, related_name='decisions')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20, choices=[('proposed', 'Proposed'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('deprecated', 'Deprecated'), ('superseded', 'Superseded')], default='proposed')),
                ('context', models.TextField(blank=True)),
                ('decision', models.TextField(blank=True)),
                ('consequences', models.TextField(blank=True)),
                ('superseded_by', models.ForeignKey('architecture.architecturedecision', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supersedes')),
                ('decided_on', models.DateField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
