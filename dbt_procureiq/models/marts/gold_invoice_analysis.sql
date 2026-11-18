{{ config(materialized='table') }}

SELECT 
    v.vendor_id,
    v.vendor_name,
    cat.category_name,
    inv.discrepancy_reason,
    COUNT(inv.invoice_id) AS total_invoices_count,
    SUM(inv.po_amount) AS total_po_baseline_amount,
    SUM(inv.invoice_amount) AS total_billed_amount,
    SUM(inv.discrepancy_amount) AS total_discrepancy_leakage,
    ROUND(AVG(inv.discrepancy_percentage), 2) AS avg_discrepancy_percentage,
    SUM(CASE WHEN inv.is_discrepancy = true THEN 1 ELSE 0 END) AS discrepant_invoices_count,
    SUM(CASE WHEN inv.payment_status = 'Disputed' THEN 1 ELSE 0 END) AS disputed_invoices_count,
    SUM(CASE WHEN inv.payment_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices_count,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_invoices') }} inv
JOIN {{ ref('stg_vendors') }} v ON inv.vendor_id = v.vendor_id
JOIN {{ source('bronze', 'bronze_categories') }} cat ON v.primary_category_id = cat.category_id
GROUP BY v.vendor_id, v.vendor_name, cat.category_name, inv.discrepancy_reason
