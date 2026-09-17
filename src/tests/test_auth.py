from auth import get_access_token


tokens = get_access_token()

print("Authentication successful!")
print(f"Access token received: {bool(tokens.get('access_token'))}")
print(f"Refresh token received: {bool(tokens.get('refresh_token'))}")