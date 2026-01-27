#!/usr/bin/env python
import re
import os

# Read the file
models_file = r"C:\Users\newwe\Desktop\tution\tutionplus\django\django_project\bank\models.py"

with open(models_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find: def save(self):
# Replace with: def save(self, *args, **kwargs):
pattern = r'def save\(self\):'
replacement = r'def save(self, *args, **kwargs):'
content = re.sub(pattern, replacement, content)

# Now fix the super() calls within save methods
pattern = r'super\((\w+), self\)\.save\(\)'
replacement = r'super(\1, self).save(*args, **kwargs)'
content = re.sub(pattern, replacement, content)

# Write back
with open(models_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed all save() methods in bank/models.py")
print("✓ All save(self): changed to save(self, *args, **kwargs):")
print("✓ All super().save() calls updated to super().save(*args, **kwargs)")
