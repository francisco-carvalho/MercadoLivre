CREATE TABLE IF NOT EXISTS mercado_livre_items (
    item_id VARCHAR(50),
    seller_id BIGINT,
    price NUMERIC(18, 2),
    currency_id VARCHAR(10),
    warranty TEXT,
    condition VARCHAR(20),
    shipping_mode VARCHAR(50),
    logistic_type VARCHAR(50),
    free_shipping BOOLEAN,
    job_run TIMESTAMP NOT NULL,
    PRIMARY KEY (item_id, job_run)
);

CREATE TABLE IF NOT EXISTS currency_conversions (
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    rate NUMERIC(18,8) NOT NULL,
    creation_date TIMESTAMP,
    valid_until TIMESTAMP,
    job_run TIMESTAMP NOT NULL
);