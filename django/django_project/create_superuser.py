#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User

# Check for superusers
admins = User.objects.filter(is_superuser=True)
print(f"Superusers in database: {admins.count()}")
for user in admins:
    print(f"  - {user.username}")

if admins.count() == 0:
    print("\nCreating superuser: admin")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Superuser created!")
    print("  Username: admin")
    print("  Password: admin123")
