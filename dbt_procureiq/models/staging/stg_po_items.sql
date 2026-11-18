{{ config(materialized='view') }}

SELECT
    TRIM(line_item_id) AS line_item_id,
    TRIM(po_id) AS po_id,
    CAST(line_number AS INTEGER) AS line_number,
    TRIM(product_id) AS product_id,
    CAST(quantity_ordered AS INTEGER) AS quantity_ordered,
    CAST(unit_price AS NUMERIC(12, 2)) AS unit_price,
    CAST(line_total_amount AS NUMERIC(15, 2)) AS line_total_amount,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_purchase_order_items') }}
WHERE line_item_id IS NOT NULL AND quantity_ordered > 0
