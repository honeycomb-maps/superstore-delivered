-- fact_orders.sql
{{ config(materialized='table') }}

WITH order_info AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        ship_date,
        ship_mode,
        delivery_address,
        delivery_lat,
        delivery_lon,
        hex(h3_latlng_to_cell(delivery_lat, delivery_lon, 10)) as delivery_h3,
        SUM(sales) as total_sales,
        SUM(quantity) as total_quantity,
        SUM(profit) as total_profit
    FROM {{ ref('stg_orders') }}
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9
)

SELECT
    order_id,
    customer_id,
    order_date,
    ship_date,
    ship_mode,
    delivery_address,
    delivery_lat,
    delivery_lon,
    delivery_h3,
    total_sales,
    total_quantity,
    total_profit
FROM order_info
