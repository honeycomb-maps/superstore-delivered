-- models/order_locations_delivery_success.sql

{{ config(materialized='table') }}

SELECT
    o.order_id,
    o.delivery_lat AS latitude,
    o.delivery_lon AS longitude,
    CASE
        WHEN d.delivery_status = 'Delivered' THEN TRUE
        WHEN d.delivery_status = 'Failed' THEN FALSE
        ELSE NULL  -- for any other status or if status is unknown
    END AS delivery_successful
FROM {{ ref('fact_orders') }} o
LEFT JOIN {{ ref('fact_deliveries') }} d ON o.order_id = d.order_id