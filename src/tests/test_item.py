import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

url = "https://api.mercadolibre.com/items"

params = {
    "ids": "MLA599260060,MLA594239600",
    "attributes": "id,price,category_id,title",
}

headers = {
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text[:2000]}")