{{ config(materialized='view') }}

SELECT
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    TRIM(department_id) AS department_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(promised_delivery_date AS DATE) AS promised_delivery_date,
    TRIM(po_status) AS po_status,
    TRIM(currency) AS currency,
    CAST(total_po_amount AS NUMERIC(15, 2)) AS total_po_amount,
    TRIM(buyer_name) AS buyer_name,
    CASE WHEN po_status = 'Fulfilled' THEN 1 ELSE 0 END AS is_fulfilled,
    CASE WHEN po_status = 'Cancelled' THEN 1 ELSE 0 END AS is_cancelled,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_purchase_orders') }}
WHERE po_id IS NOT NULL
