import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

url = "https://api.mercadolibre.com/users/2"

headers = {
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    headers=headers,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text[:2000]}")