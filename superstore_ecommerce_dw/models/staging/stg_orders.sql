WITH source AS (
    SELECT * FROM {{ source('raw_data', 'ecommerce_orders') }}
)

SELECT
    order_id,
    CAST(customer_id AS INTEGER) AS customer_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(ship_date AS DATE) AS ship_date,
    ship_mode,
    delivery_address,
    CAST(delivery_lat AS DECIMAL(10,8)) AS delivery_lat,
    CAST(delivery_lon AS DECIMAL(11,8)) AS delivery_lon,
    zip_code
FROM source