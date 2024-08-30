WITH source AS (
    SELECT * FROM {{ source('raw_data', 'delivery_data') }}
)

SELECT
    CAST(delivery_id AS INTEGER) AS delivery_id,
    order_id,
    CAST(estimated_delivery_date AS DATE) AS estimated_delivery_date,
    CAST(actual_delivery_date AS DATE) AS actual_delivery_date,
    delivery_status
FROM source