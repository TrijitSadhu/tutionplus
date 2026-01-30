import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genai', '0018_auto_20260128_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobFetch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_url', models.TextField(help_text='URL or identifier for the fetch job')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_date', models.DateField(db_index=True, default=datetime.date.today)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], db_index=True, default='PENDING', max_length=20)),
                ('fetch_log', models.TextField(blank=True, help_text='Log of timestamps, decisions, and errors for this fetch job', null=True)),
                ('prompt', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='job_fetches', to='genai.LLMPrompt')),
            ],
            options={
                'verbose_name': 'Job Fetch',
                'verbose_name_plural': 'Job Fetches',
                'ordering': ['-created_date'],
                'indexes': [
                    models.Index(fields=['status', 'created_date'], name='jobfetch_status_created_idx'),
                    models.Index(fields=['is_active', 'status'], name='jobfetch_active_status_idx'),
                ],
            },
        ),
    ]