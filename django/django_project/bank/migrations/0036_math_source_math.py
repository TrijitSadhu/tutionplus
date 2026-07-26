from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0035_math_translated_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='math',
            name='source_math',
            field=models.ForeignKey(
                blank=True,
                help_text='If this question was copied/rephrased from another, that original question.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='variants',
                to='bank.math',
                db_index=True,
            ),
        ),
    ]
