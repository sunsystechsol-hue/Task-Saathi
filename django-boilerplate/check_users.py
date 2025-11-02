#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')
django.setup()

from users.models import Users

print("\n=== All Users in Database ===")
for user in Users.objects.all():
    role = getattr(user, 'userRole', 'NO_ROLE_FIELD')
    print(f"Email: {user.email}")
    print(f"  - ID: {user.id}")
    print(f"  - Role: {role}")
    print(f"  - Active: {user.is_active}")
    print(f"  - Verified: {user.isVerified}")
    print()
