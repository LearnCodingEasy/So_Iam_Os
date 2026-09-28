from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("learning", "0002_alter_knowledgeapplication_knowledge_item"),
    ]
    operations = [
        migrations.CreateModel(
            name="UserLearningSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("daily_learning_tasks", models.PositiveSmallIntegerField(default=5)),
                ("task_generation_enabled", models.BooleanField(default=True)),
                ("preferred_learning_time", models.TimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("current_learning_goal", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="focused_by_users", to="learning.learninggoal")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="learning_settings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.CheckConstraint(condition=models.Q(("daily_learning_tasks__gte", 1), ("daily_learning_tasks__lte", 10)), name="learning_tasks_1_10")]},
        ),
    ]
