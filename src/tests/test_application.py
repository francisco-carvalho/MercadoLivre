import os

import requests
from dotenv import load_dotenv

from auth import get_access_token


load_dotenv()


access_token = get_access_token()
app_id = os.getenv("MELI_CLIENT_ID")

url = f"https://api.mercadolibre.com/applications/{app_id}"

headers = {
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(
    url,
    headers=headers,
    timeout=30,
)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text}")