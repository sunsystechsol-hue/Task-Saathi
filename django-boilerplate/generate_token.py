import os
import django
import sys
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings.dev')
django.setup()

from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Users

def generate_token_for_user(username):
    try:
        user = Users.objects.get(email=username)
        refresh = RefreshToken.for_user(user)
        
        print("\n=== TOKEN INFORMATION ===")
        print(f"User: {user.username} (ID: {user.id})")
        print(f"Access Token: {refresh.access_token}")
        print(f"Refresh Token: {refresh}")
        print("\nCopy the access token to use in your browser console:")
        print("\nlocalStorage.setItem('token', '" + str(refresh.access_token) + "');")
        print("localStorage.setItem('refresh_token', '" + str(refresh) + "');")
        print("localStorage.setItem('user_id', '" + str(user.id) + "');")
        print("localStorage.setItem('loggedIn', 'true');")
        
    except Users.DoesNotExist:
        print(f"User with email '{username}' does not exist.")
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_token.py <username>")
        sys.exit(1)
        
    username = sys.argv[1]
    generate_token_for_user(username)