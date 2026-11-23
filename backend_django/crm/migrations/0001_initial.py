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
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='crm_companies')),
                ('name', models.CharField(max_length=200)),
                ('industry', models.CharField(max_length=120, blank=True)),
                ('website', models.URLField(blank=True)),
                ('size', models.CharField(max_length=60, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='crm_contacts')),
                ('company', models.ForeignKey('crm.company', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120, blank=True)),
                ('email', models.EmailField(blank=True)),
                ('phone', models.CharField(max_length=40, blank=True)),
                ('job_title', models.CharField(max_length=160, blank=True)),
                ('source', models.CharField(max_length=120, blank=True)),
                ('status', models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='active')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='crm_interactions')),
                ('contact', models.ForeignKey('crm.contact', on_delete=django.db.models.deletion.CASCADE, related_name='interactions')),
                ('interaction_type', models.CharField(max_length=20, choices=[('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting'), ('message', 'Message'), ('note', 'Note')], default='note')),
                ('subject', models.CharField(max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('occurred_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('follow_up_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-occurred_at']},
        ),
        migrations.CreateModel(
            name='CustomerRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='crm_relationships')),
                ('contact', models.OneToOneField('crm.contact', on_delete=django.db.models.deletion.CASCADE, related_name='relationship')),
                ('stage', models.CharField(max_length=20, choices=[('lead', 'Lead'), ('prospect', 'Prospect'), ('customer', 'Customer'), ('partner', 'Partner'), ('churned', 'Churned')], default='lead')),
                ('health_score', models.PositiveSmallIntegerField(default=50)),
                ('next_step', models.TextField(blank=True)),
                ('stage_changed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-updated_at']},
        ),
    ]
