import requests

from auth import get_access_token

def get_product_items(
    product_id: str,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = f"https://api.mercadolibre.com/products/{product_id}/items"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    result = get_product_items(
        "MLA45502235",
        limit=50,
        offset=0,
    )

    print(result["paging"])
    print(f"Items returned: {len(result['results'])}")