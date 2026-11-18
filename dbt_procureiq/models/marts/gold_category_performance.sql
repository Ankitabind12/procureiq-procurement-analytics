{{ config(materialized='table') }}

SELECT 
    cat.category_id,
    cat.category_name,
    cat.spend_tier,
    COUNT(DISTINCT po.vendor_id) AS active_suppliers_count,
    COUNT(DISTINCT poi.product_id) AS active_skus_count,
    COUNT(DISTINCT po.po_id) AS total_orders_placed,
    SUM(poi.line_total_amount) AS total_category_spend,
    ROUND(AVG(poi.unit_price), 2) AS avg_unit_price,
    ROUND(AVG(poi.quantity_ordered), 2) AS avg_order_quantity,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_categories') }} cat
JOIN {{ ref('stg_vendors') }} v ON cat.category_id = v.primary_category_id
JOIN {{ ref('stg_purchase_orders') }} po ON v.vendor_id = po.vendor_id
JOIN {{ ref('stg_po_items') }} poi ON po.po_id = poi.po_id
GROUP BY cat.category_id, cat.category_name, cat.spend_tier
