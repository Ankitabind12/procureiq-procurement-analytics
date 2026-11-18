{{ config(materialized='view') }}

SELECT
    TRIM(vendor_id) AS vendor_id,
    TRIM(vendor_name) AS vendor_name,
    TRIM(primary_category_id) AS primary_category_id,
    TRIM(country) AS country,
    TRIM(city) AS city,
    LOWER(TRIM(contact_email)) AS contact_email,
    TRIM(payment_terms) AS payment_terms,
    TRIM(risk_rating) AS risk_rating,
    TRIM(vendor_status) AS vendor_status,
    CAST(registration_date AS DATE) AS registration_date,
    CAST(delivery_reliability_bias AS NUMERIC(6, 4)) AS baseline_reliability,
    CAST(price_competitiveness_bias AS NUMERIC(6, 4)) AS baseline_price_index,
    CAST(quality_defect_rate_bias AS NUMERIC(6, 4)) AS baseline_defect_rate,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_vendors') }}
WHERE vendor_id IS NOT NULL
