#!/usr/bin/env python
"""Fix all save() methods in bank/models.py to accept *args and **kwargs"""

import re

models_file = r"C:\Users\newwe\Desktop\tution\tutionplus\django\django_project\bank\models.py"

# Read the file
with open(models_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("Reading file...")
print(f"File size: {len(content)} characters")

# Count occurrences before fixing
before_count = len(re.findall(r'def save\(self\):', content))
print(f"\nFound {before_count} save(self): methods to fix")

# Fix 1: Replace all "def save(self):" with "def save(self, *args, **kwargs):"
content = re.sub(
    r'def save\(self\):',
    r'def save(self, *args, **kwargs):',
    content
)

# Fix 2: Replace all "super(ClassName, self).save()" with "super(ClassName, self).save(*args, **kwargs)"
content = re.sub(
    r'super\((\w+), self\)\.save\(\)',
    r'super(\1, self).save(*args, **kwargs)',
    content
)

# Count occurrences after fixing
after_count = len(re.findall(r'def save\(self, \*args, \*\*kwargs\):', content))
print(f"Fixed {after_count} save() methods")

# Write back
with open(models_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✓ Successfully fixed all save() methods in bank/models.py")
print(f"✓ Changed {before_count} save(self): to save(self, *args, **kwargs):")
print(f"✓ Updated super().save() calls to include *args, **kwargs")
