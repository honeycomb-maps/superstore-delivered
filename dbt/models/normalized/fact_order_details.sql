-- fact_order_details.sql
{{ config(materialized='table') }}

SELECT
    order_id,
    product_id,
    sales,
    quantity,
    discount,
    profit
FROM {{ ref('stg_orders') }}
