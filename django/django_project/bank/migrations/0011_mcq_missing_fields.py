# Generated migration to add missing fields to MCQ model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0010_auto_20260124_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcq',
            name='important_day',
            field=models.BooleanField(default=False),
        ),
    ]
