{{ config(materialized='table') }}

SELECT 
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    dept.department_name,
    dept.cost_center,
    cat.category_name,
    cat.spend_tier,
    COUNT(po.po_id) AS total_po_count,
    SUM(po.total_po_amount) AS total_spend,
    ROUND(AVG(po.total_po_amount), 2) AS avg_po_amount,
    SUM(CASE WHEN po.po_status = 'Fulfilled' THEN po.total_po_amount ELSE 0 END) AS fulfilled_spend,
    SUM(CASE WHEN po.po_status = 'Cancelled' THEN po.total_po_amount ELSE 0 END) AS cancelled_spend,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_purchase_orders') }} po
JOIN {{ source('bronze', 'bronze_date_dimension') }} d ON po.order_date = CAST(d.full_date AS DATE)
JOIN {{ source('bronze', 'bronze_departments') }} dept ON po.department_id = dept.department_id
JOIN {{ ref('stg_vendors') }} v ON po.vendor_id = v.vendor_id
JOIN {{ source('bronze', 'bronze_categories') }} cat ON v.primary_category_id = cat.category_id
GROUP BY d.year, d.quarter, d.month, d.month_name, dept.department_name, dept.cost_center, cat.category_name, cat.spend_tier
