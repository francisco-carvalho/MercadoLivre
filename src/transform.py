from datetime import datetime


def transform_items(items: list, config: dict, job_run) -> list:
    required_condition = config["filters"]["condition"]

    transformed = []

    for item in items:
        if item.get("condition") != required_condition:
            continue

        shipping = item.get("shipping", {})

        transformed.append({
            "item_id": item.get("item_id"),
            "seller_id": item.get("seller_id"),
            "price": item.get("price"),
            "currency_id": item.get("currency_id"),
            "warranty": item.get("warranty"),
            "condition": item.get("condition"),
            "shipping_mode": shipping.get("mode"),
            "logistic_type": shipping.get("logistic_type"),
            "free_shipping": shipping.get("free_shipping"),
            "job_run": job_run,
        })

    return transformed


def transform_currency_conversion(conversion: dict, job_run) -> dict:
    return {
        "from_currency": conversion["currency_base"],
        "to_currency": conversion["currency_quote"],
        "rate": conversion["rate"],
        "creation_date": conversion["creation_date"],
        "valid_until": conversion["valid_until"],
        "job_run": job_run,
    }