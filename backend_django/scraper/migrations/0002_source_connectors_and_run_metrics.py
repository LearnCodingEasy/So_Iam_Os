from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("scraper", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(model_name="website", name="source_type", field=models.CharField(choices=[("json", "JSON / REST API"), ("rss", "RSS / Atom"), ("html", "Public HTML")], default="html", max_length=12)),
        migrations.AddField(model_name="website", name="config", field=models.JSONField(blank=True, default=dict, help_text="Connector settings; never store secrets here.")),
        migrations.AddField(model_name="website", name="created_by", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="scraper_websites", to=settings.AUTH_USER_MODEL)),
        migrations.AddField(model_name="website", name="last_run_at", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="website", name="last_status", field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name="website", name="last_error", field=models.TextField(blank=True)),
        migrations.AddField(model_name="website", name="request_timeout", field=models.PositiveSmallIntegerField(default=15)),
        migrations.AddField(model_name="scrapingjob", name="items_created", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="scrapingjob", name="items_updated", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="scrapingjob", name="items_duplicate", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="scrapingjob", name="trigger_type", field=models.CharField(choices=[("manual", "Manual"), ("scheduled", "Scheduled")], default="manual", max_length=20)),
    ]
