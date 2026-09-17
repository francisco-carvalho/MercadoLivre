import requests
from auth import get_access_token


def search_products():
    tokens = get_access_token()
    access_token = tokens["access_token"]

    url = "https://api.mercadolibre.com/products/search"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }


    ## Not a 100% match with q. Need to filter after
    params = {
        "site_id": "MLA",
        "q": "Samsung Galaxy S24",
        "limit": 50,
        "domain_id": "MLA-CELLPHONES",
        "model": "S24",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    products = []

    for offset in range(0, 500, 50):
        params = {
            "site_id": "MLA",
            "q": "Samsung Galaxy S24",
            "limit": 50,
            "offset": offset,
            "domain_id": "MLA-CELLPHONES",
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()


        for product in data.get("results", []):
            name = product.get("name", "").lower()

            if (
                "samsung galaxy s24" in name
                and "ultra" not in name
                and "plus" not in name
                and "fe" not in name
            ):
                products.append({
                    "id": product.get("id"),
                    "name": product.get("name"),
                    "domain_id": product.get("domain_id"),
                })

    #deduplicate
    unique_products = {}

    for product in products:
        unique_products[product["id"]] = product

    products = list(unique_products.values())


    return {
        "paging": data.get("paging"),
        "products": products,
    }


if __name__ == "__main__":
    result = search_products()

    print("PAGING:")
    print(result["paging"])

    print("\nPRODUCTS:")

    for product in result["products"]:
        print(product)

