from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mocktest", "0003_add_mcq_model_to_rule"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="mocktestquestion",
            unique_together={("mock_test", "mcq_model", "mcq_id")},
        ),
    ]
