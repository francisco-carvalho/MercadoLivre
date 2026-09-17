import requests


url = "https://api.mercadolibre.com/sites/MLA"

response = requests.get(
    url,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text}")