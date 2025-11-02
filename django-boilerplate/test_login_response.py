#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')
django.setup()

from users.models import Users
from users.views.login import CustomTokenPairSerializer

print("\n=== Testing Login Response ===\n")

# Test with employer account
test_data = {
    'email': 'employer@test.com',
    'password': 'testpass123'
}

serializer = CustomTokenPairSerializer(data=test_data)
if serializer.is_valid():
    response_data = serializer.validated_data
    print("Login Response:")
    print(json.dumps(response_data, indent=2, default=str))
    print("\n✓ Login successful!")
    print(f"✓ Access token present: {'access' in response_data}")
    print(f"✓ Refresh token present: {'refresh' in response_data}")
    print(f"✓ User data present: {'user' in response_data}")
    if 'user' in response_data:
        print(f"✓ User role: {response_data['user'].get('userRole')}")
else:
    print("❌ Login failed:")
    print(serializer.errors)
