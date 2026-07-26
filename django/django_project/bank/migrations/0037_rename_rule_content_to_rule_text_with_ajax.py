from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0036_math_source_math'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rule_math',
            old_name='rule_content',
            new_name='rule_text_with_latex',
        ),
        migrations.RenameField(
            model_name='rule_math_translation',
            old_name='rule_content',
            new_name='rule_text_with_latex',
        ),
    ]
