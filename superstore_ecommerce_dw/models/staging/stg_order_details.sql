WITH source AS (
    SELECT * FROM {{ source('raw_data', 'ecommerce_order_details') }}
)

SELECT
    order_id,
    CAST(product_id AS INTEGER) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(sales AS DECIMAL(10,2)) AS sales,
    CAST(discount AS DECIMAL(4,2)) AS discount,
    CAST(profit AS DECIMAL(10,2)) AS profit
FROM source