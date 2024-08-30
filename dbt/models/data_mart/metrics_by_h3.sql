-- metrics_by_h3.sql
{{ config(materialized='table') }}

WITH order_delivery_data AS (
    SELECT
        o.delivery_h3,
        o.order_id,
        o.total_sales,
        d.delivery_status
    FROM {{ ref('fact_orders') }} o
    LEFT JOIN {{ ref('fact_deliveries') }} d ON o.order_id = d.order_id
),

aggregated_data AS (
    SELECT
        delivery_h3,
        COUNT(DISTINCT order_id) AS number_of_orders,
        SUM(total_sales) AS total_sales,
        SUM(CASE WHEN delivery_status = 'Failed' THEN 1 ELSE 0 END) AS failed_deliveries,
        COUNT(delivery_status) AS total_deliveries
    FROM order_delivery_data
    GROUP BY delivery_h3
)

SELECT
    delivery_h3,
    number_of_orders,
    total_sales,
    failed_deliveries,
    CASE
        WHEN total_deliveries > 0 THEN CAST(failed_deliveries AS FLOAT) / total_deliveries * 100
        ELSE 0
    END AS pct_failed_deliveries
FROM aggregated_data