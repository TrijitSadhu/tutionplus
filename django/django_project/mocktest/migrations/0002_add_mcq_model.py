from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mocktest", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mocktestquestion",
            name="mcq_model",
            field=models.CharField(max_length=100, blank=True, null=True, db_index=True),
        ),
    ]
