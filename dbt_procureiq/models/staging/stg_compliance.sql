{{ config(materialized='view') }}

SELECT
    TRIM(compliance_id) AS compliance_id,
    TRIM(vendor_id) AS vendor_id,
    TRIM(document_type) AS document_type,
    CAST(issue_date AS DATE) AS issue_date,
    CAST(expiry_date AS DATE) AS expiry_date,
    TRIM(compliance_status) AS compliance_status,
    CAST(audit_score AS INTEGER) AS audit_score,
    TRIM(auditor_name) AS auditor_name,
    CASE 
        WHEN CAST(expiry_date AS DATE) < DATE '2025-11-15' THEN 'HIGH RISK - EXPIRED'
        WHEN CAST(expiry_date AS DATE) <= DATE '2025-11-15' + 45 THEN 'MEDIUM RISK - EXPIRING SOON'
        ELSE 'LOW RISK - VALID'
    END AS compliance_risk_tier,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ source('bronze', 'bronze_vendor_compliance') }}
WHERE compliance_id IS NOT NULL
