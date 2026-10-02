from django.db import migrations


class Migration(migrations.Migration):
    """
    Reconciles the source migration graph with the existing project database.

    The distributed SQLite database already contains the schema represented by
    this historical migration.  The original migration file was missing from
    the source tree, so Django could not reconstruct the applied graph.
    Keeping this migration as a no-op is intentional: it restores the graph
    without rewriting or deleting existing learning data.
    """

    dependencies = [
        ("learning", "0003_learningnote_reflection"),
    ]

    operations = []
