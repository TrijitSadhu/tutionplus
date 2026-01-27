# Generated migration to add use_playwright field to ProcessingLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genai', '0013_auto_20260127_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='processinglog',
            name='use_playwright',
            field=models.BooleanField(default=False, help_text="It's a separate download engine"),
        ),
    ]
