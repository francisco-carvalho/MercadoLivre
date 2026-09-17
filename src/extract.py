import requests

from src.auth import get_access_token


def search_products(config: dict) -> list:
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = (
        f"{config['api']['base_url']}"
        f"{config['endpoints']['product_search']}"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    products = []

    page_size = config["search"]["page_size"]
    max_pages = config["search"]["max_pages"]
    product_name_filter = config["search"]["product_name_filter"].lower()

    # Mercado Livre limits the maximum offset for this endpoint,
    # so pagination is capped by max_pages from the configuration.
    for page in range(max_pages):
        offset = page * page_size

        params = {
            "site_id": config["search"]["site_id"],
            "q": config["search"]["query"],
            "limit": page_size,
            "offset": offset,
            "domain_id": "MLA-CELLPHONES",
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        if response.status_code != 200:
            print(f"Status: {response.status_code}")
            print(f"URL: {response.url}")
            print(f"Resposta: {response.text}")

        response.raise_for_status()

        data = response.json()



        for product in data.get("results", []):
            name = product.get("name", "").lower()

            if (
                product_name_filter in name
                and "ultra" not in name
                and "plus" not in name
                and "fe" not in name
            ):
                products.append({
                    "id": product.get("id"),
                    "name": product.get("name"),
                })

    # Remove dup products
    unique_products = {}

    for product in products:
        unique_products[product["id"]] = product

    return list(unique_products.values())


def get_product_items(
    product_id: str,
    config: dict,
) -> list:
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = (
        f"{config['api']['base_url']}"
        f"{config['endpoints']['product_items'].format(product_id=product_id)}"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "limit": config["search"]["page_size"],
        "offset": 0,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])

def get_currency_conversion(from_currency, to_currency, config):
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = (
        f"{config['api']['base_url']}"
        f"{config['endpoints']['currency_conversions']}/search"
    )

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

    response.raise_for_status()

    return response.json()