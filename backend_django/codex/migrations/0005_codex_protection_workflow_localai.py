from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("codex", "0004_codex_capability_registry")]

    operations = [
        migrations.CreateModel(
            name="ProtectedItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=220)),
                ("item_type", models.CharField(choices=[("file","File"),("directory","Directory"),("model","Django Model"),("api","API Endpoint"),("feature","Feature"),("component","Frontend Component"),("service","Service")], default="file", max_length=30)),
                ("path", models.CharField(blank=True, max_length=700)),
                ("target", models.CharField(blank=True, max_length=700)),
                ("reason", models.TextField(blank=True)),
                ("approved", models.BooleanField(default=False)),
                ("frozen", models.BooleanField(default=False)),
                ("rules", models.JSONField(blank=True, default=dict)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("approved_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="codex_approved_protected_items", to=settings.AUTH_USER_MODEL)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="protected_items", to="codex.projectregistry")),
            ],
            options={"ordering": ["item_type", "path", "key"]},
        ),
        migrations.CreateModel(
            name="CodexWorkflowStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=120)),
                ("name", models.CharField(max_length=220)),
                ("order", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(choices=[("pending","Pending"),("in_progress","In Progress"),("completed","Completed"),("blocked","Blocked"),("skipped","Skipped")], default="pending", max_length=30)),
                ("description", models.TextField(blank=True)),
                ("dependencies", models.JSONField(blank=True, default=list)),
                ("checks", models.JSONField(blank=True, default=list)),
                ("evidence", models.JSONField(blank=True, default=dict)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="workflow_steps", to="codex.projectregistry")),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="LocalAIJob",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("task_type", models.CharField(choices=[("summarize","Summarize"),("classify","Classify"),("metadata","Metadata"),("markdown_index","Markdown Index"),("architecture","Architecture")], default="metadata", max_length=40)),
                ("status", models.CharField(choices=[("queued","Queued"),("running","Running"),("completed","Completed"),("failed","Failed"),("cancelled","Cancelled")], default="queued", max_length=30)),
                ("input_data", models.JSONField(blank=True, default=dict)),
                ("result", models.JSONField(blank=True, default=dict)),
                ("provider", models.CharField(default="local", max_length=80)),
                ("error", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="local_ai_jobs", to="codex.projectregistry")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="protecteditem",
            constraint=models.UniqueConstraint(fields=("project","key"), name="codex_protected_item_project_key_unique"),
        ),
        migrations.AddConstraint(
            model_name="codexworkflowstep",
            constraint=models.UniqueConstraint(fields=("project","key"), name="codex_workflow_step_project_key_unique"),
        ),
    ]
