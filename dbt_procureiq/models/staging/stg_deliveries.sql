{{ config(materialized='view') }}

SELECT
    TRIM(delivery_id) AS delivery_id,
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    CAST(promised_delivery_date AS DATE) AS promised_delivery_date,
    CAST(actual_delivery_date AS DATE) AS actual_delivery_date,
    CAST(delay_days AS INTEGER) AS delay_days,
    TRIM(delivery_status) AS delivery_status,
    CASE WHEN CAST(delay_days AS INTEGER) <= 0 THEN 1 ELSE 0 END AS is_ontime,
    CASE 
        WHEN CAST(delay_days AS INTEGER) <= 0 THEN '0. On-Time'
        WHEN CAST(delay_days AS INTEGER) BETWEEN 1 AND 7 THEN '1. 1-7 Days Delay'
        WHEN CAST(delay_days AS INTEGER) BETWEEN 8 AND 14 THEN '2. 8-14 Days Delay'
        ELSE '3. 15+ Days Severe Delay'
    END AS delay_bucket,
    TRIM(quality_inspection_result) AS quality_inspection_result,
    CASE WHEN TRIM(quality_inspection_result) = 'Pass' THEN 1 ELSE 0 END AS is_quality_pass,
    CAST(defect_rate_percentage AS NUMERIC(6, 2)) AS defect_rate_percentage,
    TRIM(carrier_name) AS carrier_name,
    TRIM(tracking_number) AS tracking_number,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_deliveries') }}
WHERE delivery_id IS NOT NULL
