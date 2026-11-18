{{ config(materialized='table') }}

SELECT 
    po.po_id,
    v.vendor_name,
    dept.department_name,
    po.order_date,
    po.promised_delivery_date,
    po.po_status,
    po.total_po_amount,
    po.buyer_name,
    po.is_fulfilled,
    po.is_cancelled,
    COUNT(poi.line_item_id) AS total_line_items,
    SUM(poi.quantity_ordered) AS total_units_ordered,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_purchase_orders') }} po
JOIN {{ ref('stg_vendors') }} v ON po.vendor_id = v.vendor_id
JOIN {{ source('bronze', 'bronze_departments') }} dept ON po.department_id = dept.department_id
LEFT JOIN {{ ref('stg_po_items') }} poi ON po.po_id = poi.po_id
GROUP BY po.po_id, v.vendor_name, dept.department_name, po.order_date, po.promised_delivery_date, po.po_status, po.total_po_amount, po.buyer_name, po.is_fulfilled, po.is_cancelled
