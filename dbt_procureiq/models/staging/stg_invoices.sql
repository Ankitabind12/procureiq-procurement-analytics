{{ config(materialized='view') }}

SELECT
    TRIM(invoice_id) AS invoice_id,
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    CAST(invoice_date AS DATE) AS invoice_date,
    CAST(payment_due_date AS DATE) AS payment_due_date,
    CAST(po_amount AS NUMERIC(15, 2)) AS po_amount,
    CAST(invoice_amount AS NUMERIC(15, 2)) AS invoice_amount,
    CAST(discrepancy_amount AS NUMERIC(15, 2)) AS discrepancy_amount,
    is_discrepancy,
    TRIM(discrepancy_reason) AS discrepancy_reason,
    ROUND(CAST(discrepancy_amount AS NUMERIC) / NULLIF(CAST(po_amount AS NUMERIC), 0) * 100.0, 2) AS discrepancy_percentage,
    TRIM(payment_status) AS payment_status,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_invoices') }}
WHERE invoice_id IS NOT NULL
