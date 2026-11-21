from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("jobs_opportunity", "0003_expand_job_url_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobSourceSyncRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("celery_task_id", models.CharField(blank=True, default="", max_length=255)),
                ("status", models.CharField(choices=[("queued", "Queued"), ("running", "Running"), ("completed", "Completed"), ("failed", "Failed"), ("cancelled", "Cancelled")], default="queued", max_length=20)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("job_count", models.PositiveIntegerField(default=0)),
                ("error_message", models.TextField(blank=True, default="")),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("source", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sync_runs", to="jobs_opportunity.jobsource")),
                ("user", models.ForeignKey(on_delete=django.db.models.CASCADE, related_name="job_source_sync_runs", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["user", "-created_at"], name="jobs_sync_user_created_idx"),
                    models.Index(fields=["source", "-created_at"], name="jobs_sync_source_created_idx"),
                    models.Index(fields=["status"], name="jobs_sync_status_idx"),
                ],
            },
        ),
    ]
