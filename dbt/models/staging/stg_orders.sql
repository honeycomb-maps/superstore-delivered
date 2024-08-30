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
    CAST(delivery_lat AS DECIMAL(10,8)) AS delivery_lat,
    CAST(delivery_lon AS DECIMAL(11,8)) AS delivery_lon,
    CAST(product_id AS INTEGER) AS product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(sales AS DECIMAL(10,2)) AS sales,
    CAST(discount AS DECIMAL(4,2)) AS discount,
    CAST(profit AS DECIMAL(10,2)) AS profit
FROM source