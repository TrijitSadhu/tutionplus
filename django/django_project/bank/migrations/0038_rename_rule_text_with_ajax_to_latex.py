from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration 0037 was edited after it ran, so Django state already has
    rule_text_with_latex, but the DB columns are still rule_text_with_ajax.
    Use raw SQL to rename only the DB columns without touching Django state.
    """

    dependencies = [
        ('bank', '0037_rename_rule_content_to_rule_text_with_ajax'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE bank_rule_math RENAME COLUMN rule_text_with_ajax TO rule_text_with_latex;',
                    reverse_sql='ALTER TABLE bank_rule_math RENAME COLUMN rule_text_with_latex TO rule_text_with_ajax;',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE bank_rule_math_translation RENAME COLUMN rule_text_with_ajax TO rule_text_with_latex;',
                    reverse_sql='ALTER TABLE bank_rule_math_translation RENAME COLUMN rule_text_with_latex TO rule_text_with_ajax;',
                ),
            ],
            state_operations=[],  # Django state is already correct after edited 0037
        ),
    ]
