# Generated migration for adding content_date field to ContentSource

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('genai', '0007_llmprompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentsource',
            name='content_date',
            field=models.DateField(default=datetime.date.today, help_text='Date for which this content is relevant. Year, Month, and Date will be extracted for MCQs'),
        ),
    ]
