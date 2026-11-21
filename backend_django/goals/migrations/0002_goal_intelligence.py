import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("goals", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(model_name="goal", name="category", field=models.CharField(choices=[("personal", "Personal"), ("professional", "Professional"), ("educational", "Educational"), ("financial", "Financial"), ("health", "Health & Fitness"), ("business", "Business"), ("project", "Project"), ("other", "Other")], default="personal", max_length=24)),
        migrations.AddField(model_name="goal", name="measurement_unit", field=models.CharField(blank=True, max_length=40)),
        migrations.AddField(model_name="goal", name="initial_value", field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
        migrations.AddField(model_name="goal", name="target_value", field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
        migrations.AddField(model_name="goal", name="current_value", field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
        migrations.AddField(model_name="goal", name="related_goals", field=models.ManyToManyField(blank=True, related_name="related_to", to="goals.goal")),
        migrations.AlterField(model_name="goal", name="status", field=models.CharField(choices=[("draft", "Draft"), ("planned", "Planned"), ("active", "Active"), ("paused", "On Hold"), ("at_risk", "At Risk"), ("completed", "Completed"), ("cancelled", "Cancelled"), ("archived", "Archived")], default="active", max_length=20)),
        migrations.AddIndex(model_name="goal", index=models.Index(fields=["user", "category", "status"], name="goals_goal_user_cat_status_idx")),
        migrations.CreateModel(
            name="GoalMilestone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("sequence", models.PositiveIntegerField(default=0)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("target_date", models.DateField(blank=True, null=True)),
                ("status", models.CharField(choices=[("planned", "Planned"), ("active", "Active"), ("blocked", "Blocked"), ("completed", "Completed")], default="planned", max_length=16)),
                ("progress_percent", models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ("weight", models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ("completion_criteria", models.TextField(blank=True)),
                ("completion_evidence", models.TextField(blank=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("goal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="milestones", to="goals.goal")),
            ],
            options={"ordering": ["sequence", "target_date", "id"]},
        ),
        migrations.AddField(model_name="goalmilestone", name="depends_on", field=models.ManyToManyField(blank=True, related_name="dependent_milestones", to="goals.goalmilestone")),
        migrations.AddConstraint(model_name="goalmilestone", constraint=models.UniqueConstraint(fields=("goal", "sequence"), name="goal_milestone_seq_uniq")),
        migrations.AddIndex(model_name="goalmilestone", index=models.Index(fields=["goal", "status"], name="goals_milestone_status_idx")),
        migrations.AddIndex(model_name="goalmilestone", index=models.Index(fields=["goal", "target_date"], name="goals_milestone_target_idx")),
        migrations.CreateModel(
            name="GoalPlanProposal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("payload", models.JSONField(default=dict)),
                ("provider", models.CharField(blank=True, max_length=40)),
                ("status", models.CharField(choices=[("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=16)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("goal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="plan_proposals", to="goals.goal")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="goal_plan_proposals", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(model_name="goalplanproposal", index=models.Index(fields=["user", "status"], name="goals_plan_user_status_idx")),
        migrations.CreateModel(
            name="GoalActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("data", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("goal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activity", to="goals.goal")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="goal_activity", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(model_name="goalactivity", index=models.Index(fields=["goal", "created_at"], name="goals_activity_created_idx")),
    ]
