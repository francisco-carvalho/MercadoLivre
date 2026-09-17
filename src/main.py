import yaml
from datetime import datetime

from src.extract import (
    search_products, 
    get_product_items, 
    get_currency_conversion
)
from src.transform import (
    transform_items,
    transform_currency_conversion,
)
from src.load import (
    load_items,
    load_currency_conversion
)


def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()
    
    # Keep a single JOB_RUN timestamp across all tables for this ETL execution.
    job_run = datetime.now()

    # Extract - products
    products = search_products(config)

    # Extract - pubs
    all_items = []

    for product in products:
        items = get_product_items(
            product["id"],
            config,
        )

        all_items.extend(items)

    #Extract conversions
    conversion = get_currency_conversion(
        config["currency_conversion"]["from"],
        config["currency_conversion"]["to"],
        config,
    )

    # Transform items
    transformed_items = transform_items(
        all_items,
        config,
        job_run
    )

    #Transform conversions
    transformed_conversion = transform_currency_conversion(
        conversion,
        job_run,
)

    load_items(transformed_items)
    load_currency_conversion(transformed_conversion)

    print("Dados carregados no PostgreSQL!")

if __name__ == "__main__":
    main()