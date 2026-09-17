import requests

from auth import get_access_token


BASE_URL = "https://api.mercadolibre.com"


def search_items(site_id, query, limit=50, offset=0):
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = f"{BASE_URL}/sites/{site_id}/search"

    params = {
        "q": query,
        "limit": limit,
        "offset": offset,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()