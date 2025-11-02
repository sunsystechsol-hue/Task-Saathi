#!/usr/bin/env python
"""
Generate test tokens for testing the API in browser console
Run: python manage.py shell < generate_test_tokens.py
Or: docker exec -it tasksaathi-backend python generate_test_tokens.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from tasksaathi.models import Company

User = get_user_model()

# Create test employer
print("=" * 80)
print("CREATING TEST USERS")
print("=" * 80)

# Create employer
employer_email = "employer@test.com"
try:
    employer = User.objects.get(email=employer_email)
    print(f"✓ Employer already exists: {employer_email}")
except User.DoesNotExist:
    employer = User.objects.create_user(
        email=employer_email,
        password="testpass123",
        firstName="John",
        lastName="Employer",
        level=2,
        userRole="EMPLOYER",
        is_active=True,
        isVerified=True
    )
    print(f"✓ Created employer: {employer_email}")

# Create company for employer
try:
    company = Company.objects.get(userId=employer)
    print(f"✓ Company already exists: {company.name}")
except Company.DoesNotExist:
    company = Company.objects.create(
        name="Test Company Ltd.",
        userId=employer,
        isVerified=True,
        contactNumber="+1234567890"
    )
    print(f"✓ Created company: {company.name}")

# Create employee
employee_email = "employee@test.com"
try:
    employee = User.objects.get(email=employee_email)
    print(f"✓ Employee already exists: {employee_email}")
except User.DoesNotExist:
    employee = User.objects.create_user(
        email=employee_email,
        password="testpass123",
        firstName="Jane",
        lastName="Employee",
        level=2,
        userRole="EMPLOYEE",
        is_active=True,
        isVerified=True
    )
    print(f"✓ Created employee: {employee_email}")

# Generate tokens
print("\n" + "=" * 80)
print("GENERATED TOKENS")
print("=" * 80)

print("\n📌 EMPLOYER ACCOUNT")
print(f"Email: {employer_email}")
print(f"Password: testpass123")
employer_refresh = RefreshToken.for_user(employer)
employer_access = str(employer_refresh.access_token)
print(f"\nAccess Token (expires in 5 minutes):")
print(f"\n{employer_access}\n")

print("\n📌 EMPLOYEE ACCOUNT")
print(f"Email: {employee_email}")
print(f"Password: testpass123")
employee_refresh = RefreshToken.for_user(employee)
employee_access = str(employee_refresh.access_token)
print(f"\nAccess Token (expires in 5 minutes):")
print(f"\n{employee_access}\n")

print("\n" + "=" * 80)
print("HOW TO USE IN BROWSER CONSOLE")
print("=" * 80)
print("""
1. Open browser DevTools (F12)
2. Go to Console tab
3. Paste one of the access tokens above into localStorage:

For Employer:
localStorage.setItem('access_token', '{employer_access}');
localStorage.setItem('user_role', 'EMPLOYER');
localStorage.setItem('user_id', '{employer_id}');
localStorage.setItem('loggedIn', 'true');
localStorage.setItem('user', '{{"id": "{employer_id}", "email": "{employer_email}", "firstName": "John", "lastName": "Employer", "userRole": "EMPLOYER", "company": {{"id": "{company_id}", "name": "Test Company Ltd."}}}}');

For Employee:
localStorage.setItem('access_token', '{employee_access}');
localStorage.setItem('user_role', 'EMPLOYEE');
localStorage.setItem('user_id', '{employee_id}');
localStorage.setItem('loggedIn', 'true');
localStorage.setItem('user', '{{"id": "{employee_id}", "email": "{employee_email}", "firstName": "Jane", "lastName": "Employee", "userRole": "EMPLOYEE"}}');

4. Refresh the page and you'll be logged in!
5. Test API calls with: getTasks(), getMyTasks(), getCompanyTasks(), etc.
""")

print("\n" + "=" * 80)
print("READY FOR TESTING!")
print("=" * 80)
print(f"\n✅ Frontend available at: http://localhost:3000")
print(f"✅ Backend available at: http://localhost:8000")
print(f"✅ API Docs at: http://localhost:8000/swagger/")
print()
