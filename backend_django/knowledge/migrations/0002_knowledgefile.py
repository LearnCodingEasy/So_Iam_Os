from django.db import migrations


class Migration(migrations.Migration):
    """
    Compatibility node for the historical database migration graph.

    The delivered SQLite database contains this migration as applied, while
    the current source tree had already folded its schema changes into the
    initial knowledge migration.  Keeping a no-op node preserves the applied
    history without replaying or duplicating schema operations.
    """

    dependencies = [
        ("knowledge", "0001_initial"),
    ]

    operations = []
