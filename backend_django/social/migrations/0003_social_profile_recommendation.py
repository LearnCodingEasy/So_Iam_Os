from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("social", "0002_initial")]
    operations = [
        migrations.CreateModel(
            name="SocialProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("learning_interests", models.JSONField(blank=True, default=list)),
                ("professional_interests", models.JSONField(blank=True, default=list)),
                ("topics", models.JSONField(blank=True, default=list)),
                ("looking_for", models.JSONField(blank=True, default=list)),
                ("bio", models.TextField(blank=True)),
                ("discoverable", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="social_profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes":[models.Index(fields=["discoverable","updated_at"],name="social_profile_disc_idx")]},
        ),
        migrations.CreateModel(
            name="SocialRecommendation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("reasons", models.JSONField(blank=True, default=list)),
                ("breakdown", models.JSONField(blank=True, default=dict)),
                ("status", models.CharField(default="active", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="social_recommended_to", to=settings.AUTH_USER_MODEL)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="social_recommendations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"indexes":[models.Index(fields=["user","score"],name="social_rec_user_score_idx")],"constraints":[models.UniqueConstraint(fields=["user","candidate"],name="unique_social_recommendation")]},
        ),
    ]
