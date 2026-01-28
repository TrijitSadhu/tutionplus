from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genai', '0015_jsonimport'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE genai_jsonimport DROP COLUMN IF EXISTS subject;",
            reverse_sql="ALTER TABLE genai_jsonimport ADD COLUMN subject VARCHAR(50) NOT NULL DEFAULT '';",
        ),
    ]
