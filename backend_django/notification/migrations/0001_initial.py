from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
    ]
    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(choices=[("system","System"),("task","Task"),("goal","Goal"),("learning","Learning"),("knowledge","Knowledge"),("job","Job"),("ai","AI"),("social","Social")], default="system", max_length=30)),
                ("title", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("action_url", models.CharField(blank=True, max_length=500)),
                ("priority", models.PositiveSmallIntegerField(default=50)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("archived", models.BooleanField(default=False)),
                ("object_id", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("content_type", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="contenttypes.contenttype")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering":["-created_at"],"indexes":[models.Index(fields=["user","read_at","created_at"],name="notification_user_read_idx"),models.Index(fields=["user","type","created_at"],name="notification_user_type_idx")]},
        ),
    ]
