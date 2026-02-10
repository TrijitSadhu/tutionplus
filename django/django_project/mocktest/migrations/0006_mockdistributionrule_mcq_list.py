from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mocktest", "0005_mockdistributionrule_selected_mcq_ids"),
    ]

    operations = [
        migrations.AddField(
            model_name="mockdistributionrule",
            name="mcq_list",
            field=models.TextField(blank=True, default=""),
        ),
    ]
