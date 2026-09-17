from auth import refresh_access_token


tokens = refresh_access_token()

print("Refresh successful!")
print(f"Access token received: {bool(tokens.get('access_token'))}")
print(f"Refresh token received: {bool(tokens.get('refresh_token'))}")
print(f"Token expires in: {tokens.get('expires_in')} seconds")