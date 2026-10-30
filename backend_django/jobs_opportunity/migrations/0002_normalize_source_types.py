from django.db import migrations


def normalize_job_sources(apps, schema_editor):
    JobSource = apps.get_model("jobs_opportunity", "JobSource")
    database = schema_editor.connection.alias
    for source in JobSource.objects.using(database).all().iterator():
        changed = False
        if source.source_type == "html_scraper":
            source.source_type = "scraper"
            changed = True
        config = dict(source.config or {})
        if "tos_confirmed" in config:
            legacy_confirmation = bool(config.pop("tos_confirmed"))
            config.setdefault("terms_confirmed", legacy_confirmation)
            changed = True
        if changed:
            source.config = config
            source.save(using=database, update_fields=["source_type", "config"])


def reverse_normalize_job_sources(apps, schema_editor):
    # No reverse transformation: restoring the obsolete choice would make the
    # affected source records invalid against the current model choices.
    pass


class Migration(migrations.Migration):
    dependencies = [("jobs_opportunity", "0001_initial")]
    operations = [migrations.RunPython(normalize_job_sources, reverse_normalize_job_sources)]
