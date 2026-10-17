"""Compatibility migration for the Codex migration history.

The distributed 0001_initial migration already contains the Codex conversation,
analysis, and message models. The original project archive retained compiled
0002/0003 migration artifacts but not their source files. Keeping these
migration nodes as no-ops preserves the historical graph without attempting
to recreate tables that already exist after 0001.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("codex", "0001_initial"),
    ]

    operations = []
