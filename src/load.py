import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_items(items):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            for item in items:
                cursor.execute(
                    """
                    INSERT INTO mercado_livre_items (
                        item_id,
                        seller_id,
                        price,
                        currency_id,
                        warranty,
                        condition,
                        shipping_mode,
                        logistic_type,
                        free_shipping,
                        job_run
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        item["item_id"],
                        item["seller_id"],
                        item["price"],
                        item["currency_id"],
                        item["warranty"],
                        item["condition"],
                        item["shipping_mode"],
                        item["logistic_type"],
                        item["free_shipping"],
                        item["job_run"],
                    ),
                )

        connection.commit()

    finally:
        connection.close()


def load_currency_conversion(conversion):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO currency_conversions (
                    from_currency,
                    to_currency,
                    rate,
                    creation_date,
                    valid_until,
                    job_run
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    conversion["from_currency"],
                    conversion["to_currency"],
                    conversion["rate"],
                    conversion["creation_date"],
                    conversion["valid_until"],
                    conversion["job_run"],
                ),
            )

        connection.commit()
    finally:
        connection.close()