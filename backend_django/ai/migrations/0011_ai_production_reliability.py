from django.conf import settings
from django.db import migrations, models
import django.db.models.constraints




def repair_missing_ai_tables(apps, schema_editor):
    """Repair schema drift from older releases before adding reliability fields.

    Some installations recorded historical migrations while one or more AI tables
    were manually removed.  Creating only missing historical tables is safe and
    lets the normal migration operations add the new columns afterwards.
    """
    connection = schema_editor.connection
    existing = set(connection.introspection.table_names())
    model_names = [
        "AIConversation", "AIMessage", "AIPromptProfile", "AIProviderCredential",
        "AISettings", "AIExecution", "AIUsageRecord", "AIAuditLog",
        "AIBudgetPolicy", "AIFeedback", "AIWorkflowDefinition", "AIWorkflowRun",
    ]
    for name in model_names:
        model = apps.get_model("ai", name)
        table = model._meta.db_table
        if table not in existing:
            schema_editor.create_model(model)
            existing.add(table)


def noop_reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [("ai", "0010_repair_aiexecution_requested_provider")]

    operations = [
        migrations.RunPython(repair_missing_ai_tables, noop_reverse),
        migrations.AddField("aisettings", "streaming_enabled", models.BooleanField(default=True)),
        migrations.AddField("aisettings", "temperature", models.FloatField(default=0.7)),
        migrations.AddField("aisettings", "timeout_seconds", models.PositiveIntegerField(default=35)),
        migrations.AddField("aisettings", "fallback_enabled", models.BooleanField(default=True)),
        migrations.AddField("aiprovidercredential", "status", models.CharField(default="needs_review", max_length=20)),
        migrations.AddField("aiprovidercredential", "last_used_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aiprovidercredential", "last_validated_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aiconversation", "archived_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aiconversation", "deleted_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aiconversation", "last_message_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aiconversation", "message_count", models.PositiveIntegerField(default=0)),
        migrations.AddField("aiexecution", "attempt_number", models.PositiveSmallIntegerField(default=1)),
        migrations.AddField("aiexecution", "external_request_id", models.CharField(default="", max_length=255)),
        migrations.AddField("aiexecution", "idempotency_key", models.CharField(default="", max_length=255)),
        migrations.AddField("aiusagerecord", "currency", models.CharField(default="USD", max_length=8)),
        migrations.AddField("aiusagerecord", "pricing_version", models.CharField(blank=True, default="", max_length=64)),
        migrations.AddField("aiusagerecord", "cached_input_tokens", models.PositiveIntegerField(default=0)),
        migrations.AddField("aiusagerecord", "actual_cost", models.DecimalField(blank=True, decimal_places=8, max_digits=14, null=True)),
        migrations.AddField("aiusagerecord", "cost_source", models.CharField(default="estimated", max_length=32)),
        migrations.AddField("aiauditlog", "ip_address", models.GenericIPAddressField(blank=True, null=True)),
        migrations.AddField("aiauditlog", "user_agent", models.TextField(blank=True, default="")),
        migrations.AddField("aiauditlog", "request_id", models.CharField(blank=True, default="", max_length=255)),
        migrations.AddField("aifeedback", "feedback_category", models.CharField(blank=True, default="", max_length=80)),
        migrations.AddField("aifeedback", "model_version", models.CharField(blank=True, default="", max_length=120)),
        migrations.AddField("aifeedback", "reviewed_at", models.DateTimeField(blank=True, null=True)),
        migrations.AddField("aifeedback", "rating", models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField("aiworkflowdefinition", "schema_version", models.CharField(default="1.0", max_length=32)),
        migrations.AddField("aiworkflowrun", "execution", models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name="workflow_runs", to="ai.aiexecution")),
        migrations.AddField("aiworkflowrun", "workflow_version", models.PositiveIntegerField(default=1)),
        migrations.AddField("aiworkflowrun", "current_node_id", models.CharField(blank=True, default="", max_length=255)),
        migrations.AddField("aiworkflowrun", "retry_count", models.PositiveSmallIntegerField(default=0)),
        migrations.AddConstraint("aiexecution", models.UniqueConstraint(condition=~models.Q(idempotency_key=""), fields=("user", "idempotency_key"), name="unique_ai_execution_idempotency_key")),
        migrations.CreateModel(
            name="AIBudgetReservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("idempotency_key", models.CharField(max_length=255)),
                ("reserved_cost", models.DecimalField(decimal_places=8, default=0, max_digits=14)),
                ("reserved_tokens", models.PositiveBigIntegerField(default=0)),
                ("status", models.CharField(choices=[("reserved","Reserved"),("settled","Settled"),("released","Released")], default="reserved", max_length=20)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("policy", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="reservations", to="ai.aibudgetpolicy")),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="ai_budget_reservations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes":[models.Index(fields=["user","status","expires_at"], name="ai_aibudget_user_id_8b8c65_idx")]},
        ),
        migrations.AddConstraint("aibudgetreservation", models.UniqueConstraint(fields=("user","idempotency_key"), name="unique_ai_budget_reservation")),
    ]
