{{ config(materialized='table') }}

SELECT 
    c.compliance_id,
    v.vendor_id,
    v.vendor_name,
    cat.category_name,
    c.document_type,
    c.issue_date,
    c.expiry_date,
    c.compliance_status,
    c.compliance_risk_tier,
    c.audit_score,
    c.auditor_name,
    CASE 
        WHEN c.compliance_risk_tier = 'HIGH RISK - EXPIRED' THEN 'Immediate Stop-Shipment / Audit Required'
        WHEN c.compliance_risk_tier = 'MEDIUM RISK - EXPIRING SOON' THEN 'Notify Vendor - Renewal In Progress'
        ELSE 'Active Compliant'
    END AS action_recommendation,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_compliance') }} c
JOIN {{ ref('stg_vendors') }} v ON c.vendor_id = v.vendor_id
JOIN {{ source('bronze', 'bronze_categories') }} cat ON v.primary_category_id = cat.category_id
