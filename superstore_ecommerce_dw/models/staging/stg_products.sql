WITH source AS (
    SELECT * FROM {{ source('raw_data', 'ecommerce_products') }}
)

SELECT
    CAST(product_id AS INTEGER) AS product_id,
    product_name,
    category,
    sub_category,
    CAST(price AS DECIMAL(10,2)) AS price
FROM source