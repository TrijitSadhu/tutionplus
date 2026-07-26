from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0034_add_rule_translation'),
    ]

    operations = [
        migrations.AddField(
            model_name='math',
            name='translated_language',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
