"""Repair databases where AI observability migration was recorded without its column.

The field is already part of the historical model state (introduced in 0007).
This migration only repairs the physical schema when drift is detected, making it
safe for both correctly migrated databases and databases with a partially applied
or manually altered schema.
"""
from django.db import migrations


def repair_requested_provider(apps, schema_editor):
    AIExecution = apps.get_model("ai", "AIExecution")
    connection = schema_editor.connection
    table_name = AIExecution._meta.db_table

    existing_tables = set(connection.introspection.table_names())
    if table_name not in existing_tables:
        # If 0007 was applied correctly the table exists. Failing loudly is safer
        # than silently masking a more extensive database/migration inconsistency.
        raise RuntimeError(
            f"Expected AI execution table {table_name!r} is missing; "
            "inspect the ai migration history before proceeding."
        )

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    field = AIExecution._meta.get_field("requested_provider")
    if field.column not in columns:
        schema_editor.add_field(AIExecution, field)


class Migration(migrations.Migration):
    dependencies = [("ai", "0009_remove_aiauditlog_ai_aiaudit_user_created_idx_and_more")]
    operations = [migrations.RunPython(repair_requested_provider, migrations.RunPython.noop)]
