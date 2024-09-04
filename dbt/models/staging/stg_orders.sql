WITH source AS (
    SELECT * FROM {{ source('raw_data', 'order_info') }}
)

SELECT
    order_id,
    line_item_id,
    CAST(customer_id AS INTEGER) AS customer_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(ship_date AS DATE) AS ship_date,
    ship_mode,
    delivery_address,
    delivery_lat,
    delivery_lon,
    CAST(product_id AS INTEGER) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    sales,
    discount,
    profit
FROM source