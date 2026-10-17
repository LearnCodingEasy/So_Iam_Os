"""Compatibility migration for the Codex intelligence migration node.

The distributed 0001_initial migration already contains the architecture,
policy, audit, finding, agent-run, execution-request, and change-file models
that were represented by the original 0003 migration artifact. This source
migration is intentionally a no-op so Django can build a consistent migration
graph without creating duplicate tables.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("codex", "0002_codexconversation_codexanalysis_codexmessage"),
    ]

    operations = []
