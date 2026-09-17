import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

print("Access token present:", bool(access_token))
print("Access token length:", len(access_token))

url = "https://api.mercadolibre.com/users/me"

headers = {
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    headers=headers,
    timeout=30,
)

print(f"Status code: {response.status_code}")
#print(f"Response body: {response.text}")