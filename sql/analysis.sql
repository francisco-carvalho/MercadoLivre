-- 1. Sellers with multiples publications

WITH last_job_run AS (
    SELECT MAX(job_run) AS job_run
    FROM mercado_livre_items
)

SELECT
    i.seller_id,
    COUNT(DISTINCT i.item_id) AS pub_quant
FROM mercado_livre_items i
JOIN last_job_run l
    ON i.job_run = l.job_run
GROUP BY i.seller_id
HAVING COUNT(DISTINCT i.item_id) > 1
ORDER BY pub_quant DESC;


-- -- 2. Average sold_quantitites

-- WITH last_job_run AS (
--     SELECT MAX(job_run) AS job_run
--     FROM mercado_livre_items
-- )

-- SELECT
--     seller_id,
--     AVG(sold_quantity) AS average solds
-- FROM mercado_livre_items i
-- JOIN last_job_run l
--     ON i.job_run = l.job_run
-- GROUP BY seller_id;

-- 3. Average prices in USD

WITH last_job_run AS (
    SELECT MAX(job_run) AS job_run
    FROM mercado_livre_items
)

SELECT
    AVG(i.price * c.rate) AS average_price
FROM mercado_livre_items i
JOIN currency_conversions c
    ON i.currency_id = c.from_currency
    AND c.to_currency = 'USD'
    AND i.job_run = c.job_run
JOIN last_job_run l
    ON i.job_run = l.job_run;

-- 3. Average price USD with all items
-- 3.5. Averarege prices USD without outilers IQ

WITH last_job_run AS (
    SELECT MAX(job_run) AS job_run
    FROM mercado_livre_items
),

prices AS (
    SELECT
        i.item_id,
        i.price * c.rate AS price_usd
    FROM mercado_livre_items i
    JOIN currency_conversions c
        ON i.currency_id = c.from_currency
        AND c.to_currency = 'USD'
        AND i.job_run = c.job_run
    JOIN last_job_run l
        ON i.job_run = l.job_run
),

quartiles AS (
    SELECT
        percentile_cont(0.25) WITHIN GROUP (ORDER BY price_usd) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY price_usd) AS q3
    FROM prices
),

bounds AS (
    SELECT
        q1,
        q3,
        q1 - 1.5 * (q3 - q1) AS lower_bound,
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM quartiles
)

SELECT
    AVG(p.price_usd) AS precio_promedio_usd_sin_outliers
FROM prices p
CROSS JOIN bounds b
WHERE p.price_usd BETWEEN b.lower_bound AND b.upper_bound;



-- 4. Warranty items (%)

WITH last_job_run AS (
    SELECT MAX(job_run) AS job_run
    FROM mercado_livre_items
)

SELECT
    AVG(
        CASE
            WHEN warranty IS NOT NULL
                 AND LOWER(TRIM(warranty)) <> 'sin garantía'
            THEN 1.0
            ELSE 0.0
        END
    ) * 100 AS porcentaje_con_garantia
FROM mercado_livre_items i
JOIN last_job_run l
    ON i.job_run = l.job_run;

-- 5. Shipping methods

WITH last_job_run AS (
    SELECT MAX(job_run) AS job_run
    FROM mercado_livre_items
)

SELECT
    shipping_mode,
    logistic_type,
    COUNT(*) AS itens_quant
FROM mercado_livre_items i
JOIN last_job_run l
    ON i.job_run = l.job_run
GROUP BY
    shipping_mode,
    logistic_type
ORDER BY
    itens_quant DESC;