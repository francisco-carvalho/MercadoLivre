import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

item_id = "MLB1828680414"

url = f"https://api.mercadolibre.com/items/{item_id}"

headers = {
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    headers=headers,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text[:5000]}")