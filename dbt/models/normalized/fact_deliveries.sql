-- fact_deliveries.sql
{{ config(materialized='table') }}

SELECT
    delivery_id,
    order_id,
    estimated_delivery_date,
    actual_delivery_date,
    delivery_status
FROM {{ ref('stg_deliveries') }}
