from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("jobs_opportunity", "0002_normalize_source_types")]
    operations = [
        migrations.AlterField(
            model_name="jobopportunity",
            name="url",
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
