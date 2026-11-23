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
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='metrics')),
                ('key', models.SlugField(max_length=80)),
                ('name', models.CharField(max_length=160)),
                ('unit', models.CharField(max_length=40, blank=True)),
                ('source_app', models.CharField(max_length=60, blank=True)),
                ('description', models.TextField(blank=True)),
                ('kind', models.CharField(max_length=20, choices=[('gauge', 'Gauge'), ('counter', 'Counter')], default='gauge')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name'], 'constraints': [models.UniqueConstraint(fields=['user', 'key'], name='analytics_metric_user_key_unique')]},
        ),
        migrations.CreateModel(
            name='MetricSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.ForeignKey('analytics.metric', on_delete=django.db.models.deletion.CASCADE, related_name='snapshots')),
                ('value', models.DecimalField(max_digits=20, decimal_places=4)),
                ('recorded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('dimensions', models.JSONField(default=dict, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-recorded_at']},
        ),
        migrations.CreateModel(
            name='AnalyticsEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='analytics_events')),
                ('name', models.CharField(max_length=120)),
                ('source_app', models.CharField(max_length=60, blank=True)),
                ('properties', models.JSONField(default=dict, blank=True)),
                ('occurred_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-occurred_at']},
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE, related_name='analytics_reports')),
                ('title', models.CharField(max_length=200)),
                ('report_type', models.CharField(max_length=20, choices=[('summary', 'Metric summary'), ('metric_trend', 'Metric trend'), ('events', 'Event counts')], default='summary')),
                ('period_start', models.DateField(null=True, blank=True)),
                ('period_end', models.DateField(null=True, blank=True)),
                ('parameters', models.JSONField(default=dict, blank=True)),
                ('content', models.JSONField(default=dict, blank=True)),
                ('generated_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
