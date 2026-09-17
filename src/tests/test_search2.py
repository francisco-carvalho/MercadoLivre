import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

url = "https://api.mercadolibre.com/sites/MLA/search"

headers = {
    "Authorization": f"Bearer {access_token}",
}

params = {
    "q": "Samsung Galaxy S24",
    "limit": 50,
    "offset": 0,
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text[:5000]}")