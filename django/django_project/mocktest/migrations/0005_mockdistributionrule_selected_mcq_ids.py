from django.db import migrations
from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ("mocktest", "0004_alter_mocktestquestion_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="mockdistributionrule",
            name="selected_mcq_ids",
            field=JSONField(default=list, blank=True),
        ),
    ]
