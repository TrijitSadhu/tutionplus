# Generated migration to remove skip_scraping and send_url_directly from ContentSource
# These fields were mistakenly added to ContentSource and should only be in ProcessingLog

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genai', '0012_auto_20260127_1822'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE genai_contentsource DROP COLUMN IF EXISTS skip_scraping;',
            reverse_sql='ALTER TABLE genai_contentsource ADD COLUMN skip_scraping boolean NOT NULL DEFAULT false;',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE genai_contentsource DROP COLUMN IF EXISTS send_url_directly;',
            reverse_sql='ALTER TABLE genai_contentsource ADD COLUMN send_url_directly boolean NOT NULL DEFAULT false;',
        ),
    ]
