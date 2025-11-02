import jwt
from datetime import datetime, timedelta

# Create a token manually without database connection
def create_admin_token():
    # Admin user details
    user_id = "admin-user-id"
    email = "admin@gmail.com"
    
    # Token payload
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'is_staff': True,
        'is_superuser': True,
        'level': 5
    }
    
    # Secret key - using a dummy one for demonstration
    secret_key = 'django-insecure-secret-key'
    
    # Generate token
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    # Create refresh token with longer expiry
    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_payload, secret_key, algorithm='HS256')
    
    print("\n=== TOKEN INFORMATION ===")
    print(f"User: {email}")
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
    
    print("\nCopy these commands to use in your browser console:")
    print(f"localStorage.setItem('token', '{access_token}');")
    print(f"localStorage.setItem('refresh_token', '{refresh_token}');")
    print(f"localStorage.setItem('user_id', '{user_id}');")
    print(f"localStorage.setItem('loggedIn', 'true');")

if __name__ == "__main__":
    create_admin_token()