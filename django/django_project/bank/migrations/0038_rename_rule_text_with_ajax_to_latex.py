from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration 0037 already renamed rule_content -> rule_text_with_latex on fresh DBs.
    This migration was only needed for existing DBs that had rule_text_with_ajax.
    On fresh databases this is a no-op; the SeparateDatabaseAndState below
    only runs the SQL if the column actually exists to rename.
    """

    dependencies = [
        ('bank', '0037_rename_rule_content_to_rule_text_with_ajax'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    DO $$
                    BEGIN
                        IF EXISTS (
                            SELECT 1 FROM information_schema.columns
                            WHERE table_name='bank_rule_math'
                            AND column_name='rule_text_with_ajax'
                        ) THEN
                            ALTER TABLE bank_rule_math RENAME COLUMN rule_text_with_ajax TO rule_text_with_latex;
                        END IF;
                        IF EXISTS (
                            SELECT 1 FROM information_schema.columns
                            WHERE table_name='bank_rule_math_translation'
                            AND column_name='rule_text_with_ajax'
                        ) THEN
                            ALTER TABLE bank_rule_math_translation RENAME COLUMN rule_text_with_ajax TO rule_text_with_latex;
                        END IF;
                    END $$;
                    """,
                    reverse_sql='SELECT 1;',
                ),
            ],
            state_operations=[],
        ),
    ]
