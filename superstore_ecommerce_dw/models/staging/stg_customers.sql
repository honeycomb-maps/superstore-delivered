WITH source AS (
    SELECT * FROM {{ source('raw_data', 'crm_customers') }}
)

SELECT
    CAST(customer_id AS INTEGER) AS customer_id,
    customer_name,
    email,
    phone,
    segment
FROM source