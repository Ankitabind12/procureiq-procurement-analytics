{{ config(materialized='table') }}

SELECT 
    v.vendor_id,
    v.vendor_name,
    cat.category_name,
    d.carrier_name,
    d.delay_bucket,
    COUNT(d.delivery_id) AS shipment_count,
    SUM(d.is_ontime) AS ontime_count,
    COUNT(d.delivery_id) - SUM(d.is_ontime) AS delayed_count,
    ROUND(CAST(SUM(d.is_ontime) AS NUMERIC) / NULLIF(COUNT(d.delivery_id), 0) * 100.0, 2) AS ontime_percentage,
    ROUND(AVG(d.delay_days), 2) AS avg_delay_days,
    SUM(d.is_quality_pass) AS quality_passed_count,
    ROUND(CAST(SUM(d.is_quality_pass) AS NUMERIC) / NULLIF(COUNT(d.delivery_id), 0) * 100.0, 2) AS quality_pass_percentage,
    ROUND(AVG(d.defect_rate_percentage), 2) AS avg_defect_percentage,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_deliveries') }} d
JOIN {{ ref('stg_vendors') }} v ON d.vendor_id = v.vendor_id
JOIN {{ source('bronze', 'bronze_categories') }} cat ON v.primary_category_id = cat.category_id
GROUP BY v.vendor_id, v.vendor_name, cat.category_name, d.carrier_name, d.delay_bucket
