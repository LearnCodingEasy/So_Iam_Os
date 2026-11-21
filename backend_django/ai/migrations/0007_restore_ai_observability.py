from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ai", "0006_remove_aiauditlog_ai_aiauditl_user_id_5994b6_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AIExecution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("agent", models.CharField(default="default", max_length=120)),
                ("task_type", models.CharField(default="chat", max_length=80)),
                ("requested_provider", models.CharField(blank=True, default="", max_length=50)),
                ("provider", models.CharField(blank=True, default="", max_length=50)),
                ("model", models.CharField(blank=True, default="", max_length=255)),
                ("status", models.CharField(choices=[("queued", "Queued"), ("running", "Running"), ("succeeded", "Succeeded"), ("failed", "Failed"), ("cancelled", "Cancelled")], default="queued", max_length=20)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("duration_ms", models.PositiveIntegerField(blank=True, null=True)),
                ("input_tokens", models.PositiveIntegerField(blank=True, null=True)),
                ("output_tokens", models.PositiveIntegerField(blank=True, null=True)),
                ("estimated_cost", models.DecimalField(blank=True, decimal_places=8, max_digits=14, null=True)),
                ("retry_count", models.PositiveSmallIntegerField(default=0)),
                ("fallback_count", models.PositiveSmallIntegerField(default=0)),
                ("genuine_result", models.BooleanField(default=False)),
                ("error_code", models.CharField(blank=True, default="", max_length=80)),
                ("error_message", models.TextField(blank=True, default="")),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("conversation", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="executions", to="ai.aiconversation")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_executions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [
                models.Index(fields=["user", "-created_at"], name="ai_aiexec_user_created_idx"),
                models.Index(fields=["provider", "status"], name="ai_aiexec_provider_status_idx"),
            ]},
        ),
        migrations.CreateModel(
            name="AIUsageRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.CharField(max_length=50)),
                ("model", models.CharField(blank=True, default="", max_length=255)),
                ("agent", models.CharField(blank=True, default="", max_length=120)),
                ("input_tokens", models.PositiveIntegerField(default=0)),
                ("output_tokens", models.PositiveIntegerField(default=0)),
                ("estimated_cost", models.DecimalField(decimal_places=8, default=0, max_digits=14)),
                ("is_estimated", models.BooleanField(default=True)),
                ("recorded_at", models.DateTimeField(auto_now_add=True)),
                ("execution", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="usage_record", to="ai.aiexecution")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_usage_records", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes": [
                models.Index(fields=["user", "-recorded_at"], name="ai_aiusage_user_recorded_idx"),
                models.Index(fields=["provider", "model"], name="ai_aiusage_provider_model_idx"),
            ]},
        ),
        migrations.CreateModel(
            name="AIAuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=100)),
                ("resource", models.CharField(blank=True, default="", max_length=150)),
                ("result", models.CharField(default="success", max_length=30)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("execution", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="audit_logs", to="ai.aiexecution")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_audit_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [
                models.Index(fields=["user", "-created_at"], name="ai_aiaudit_user_created_idx"),
                models.Index(fields=["action", "-created_at"], name="ai_aiaudit_action_created_idx"),
            ]},
        ),
        migrations.CreateModel(
            name="AIBudgetPolicy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("scope", models.CharField(choices=[("user", "User"), ("agent", "Agent"), ("provider", "Provider")], default="user", max_length=20)),
                ("scope_key", models.CharField(default="", max_length=120)),
                ("daily_cost_limit", models.DecimalField(blank=True, decimal_places=8, max_digits=14, null=True)),
                ("monthly_cost_limit", models.DecimalField(blank=True, decimal_places=8, max_digits=14, null=True)),
                ("daily_token_limit", models.PositiveBigIntegerField(blank=True, null=True)),
                ("monthly_token_limit", models.PositiveBigIntegerField(blank=True, null=True)),
                ("enabled", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_budget_policies", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("user", "scope", "scope_key"), name="unique_ai_budget_scope")]},
        ),
        migrations.CreateModel(
            name="AIFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sentiment", models.CharField(choices=[("like", "Like"), ("dislike", "Dislike")], max_length=10)),
                ("reason", models.CharField(blank=True, default="", max_length=255)),
                ("comment", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("message", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="ai.aimessage")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_feedback", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("user", "message"), name="unique_ai_feedback_user_message")]},
        ),
        migrations.CreateModel(
            name="AIWorkflowDefinition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True, default="")),
                ("graph", models.JSONField(default=dict)),
                ("version", models.PositiveIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_workflows", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("user", "name", "version"), name="unique_ai_workflow_version")], "indexes": [models.Index(fields=["user", "-updated_at"], name="ai_aiworkfl_user_updated_idx")]},
        ),
        migrations.CreateModel(
            name="AIWorkflowRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("queued", "Queued"), ("running", "Running"), ("succeeded", "Succeeded"), ("failed", "Failed"), ("cancelled", "Cancelled")], default="queued", max_length=20)),
                ("input_data", models.JSONField(blank=True, default=dict)),
                ("output_data", models.JSONField(blank=True, default=dict)),
                ("error", models.TextField(blank=True, default="")),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_workflow_runs", to=settings.AUTH_USER_MODEL)),
                ("workflow", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="ai.aiworkflowdefinition")),
            ],
            options={"ordering": ["-created_at"], "indexes": [
                models.Index(fields=["user", "-created_at"], name="ai_aiworkfl_user_created_idx"),
                models.Index(fields=["workflow", "-created_at"], name="ai_aiworkfl_workflow_created_idx"),
            ]},
        ),
    ]
