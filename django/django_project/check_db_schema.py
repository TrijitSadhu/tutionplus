import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'genai_jsonimport' ORDER BY ordinal_position")
columns = cursor.fetchall()
print('Database columns in genai_jsonimport:')
for col in columns:
    print('  -', col[0])
