import requests

from auth import get_access_token


tokens = get_access_token()
access_token = tokens["access_token"]

from_currency = "BRL"
to_currency = "USD"

url = "https://api.mercadolibre.com/currency_conversions/search"

params = {
    "from": from_currency,
    "to": to_currency,
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
print(f"Response body: {response.text[:5000]}")