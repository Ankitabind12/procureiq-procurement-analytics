{{ config(materialized='table') }}

WITH vendor_po_stats AS (
    SELECT 
        po.vendor_id,
        COUNT(po.po_id) AS total_orders,
        SUM(po.total_po_amount) AS total_spend,
        SUM(po.is_fulfilled) AS fulfilled_orders,
        SUM(po.is_cancelled) AS cancelled_orders,
        ROUND(CAST(SUM(po.is_fulfilled) AS NUMERIC) / NULLIF(COUNT(po.po_id), 0) * 100.0, 2) AS po_fulfilment_rate
    FROM {{ ref('stg_purchase_orders') }} po
    GROUP BY po.vendor_id
),
vendor_delivery_stats AS (
    SELECT 
        d.vendor_id,
        COUNT(d.delivery_id) AS total_deliveries,
        SUM(d.is_ontime) AS ontime_deliveries,
        ROUND(CAST(SUM(d.is_ontime) AS NUMERIC) / NULLIF(COUNT(d.delivery_id), 0) * 100.0, 2) AS ontime_delivery_rate,
        ROUND(AVG(d.delay_days), 2) AS avg_delay_days,
        SUM(d.is_quality_pass) AS quality_passed_deliveries,
        ROUND(CAST(SUM(d.is_quality_pass) AS NUMERIC) / NULLIF(COUNT(d.delivery_id), 0) * 100.0, 2) AS quality_pass_rate,
        ROUND(AVG(d.defect_rate_percentage), 2) AS avg_defect_rate
    FROM {{ ref('stg_deliveries') }} d
    GROUP BY d.vendor_id
),
vendor_compliance_stats AS (
    SELECT 
        c.vendor_id,
        COUNT(c.compliance_id) AS total_certs,
        ROUND(AVG(c.audit_score), 2) AS avg_audit_score,
        SUM(CASE WHEN c.compliance_risk_tier = 'HIGH RISK - EXPIRED' THEN 1 ELSE 0 END) AS expired_certs_count
    FROM {{ ref('stg_compliance') }} c
    GROUP BY c.vendor_id
)
SELECT 
    v.vendor_id,
    v.vendor_name,
    v.primary_category_id,
    v.country,
    v.city,
    v.payment_terms,
    v.risk_rating,
    v.vendor_status,
    COALESCE(pos.total_orders, 0) AS total_orders,
    COALESCE(pos.total_spend, 0.0) AS total_spend,
    COALESCE(pos.po_fulfilment_rate, 0.0) AS po_fulfilment_rate,
    COALESCE(pos.cancelled_orders, 0) AS cancelled_orders,
    COALESCE(del.total_deliveries, 0) AS total_deliveries,
    COALESCE(del.ontime_delivery_rate, 85.0) AS ontime_delivery_rate,
    COALESCE(del.avg_delay_days, 0.0) AS avg_delay_days,
    COALESCE(del.quality_pass_rate, 90.0) AS quality_pass_rate,
    COALESCE(comp.avg_audit_score, 80.0) AS avg_compliance_score,
    COALESCE(comp.expired_certs_count, 0) AS expired_certs_count,
    
    -- 4-Pillar Transparent Scoring (Delivery 35%, Price 25%, Quality 25%, Compliance 15%)
    ROUND(COALESCE(del.ontime_delivery_rate, 85.0) * 0.35, 2) AS delivery_reliability_score,
    ROUND(25.0, 2) AS price_competitiveness_score,
    ROUND(COALESCE(del.quality_pass_rate, 90.0) * 0.25, 2) AS product_quality_score,
    ROUND((COALESCE(comp.avg_audit_score, 80.0)) * 0.15, 2) AS compliance_score,
    
    ROUND(
        (COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) +
        25.0 +
        (COALESCE(del.quality_pass_rate, 90.0) * 0.25) +
        ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15),
        2
    ) AS composite_performance_score,
    
    CASE 
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) + 25.0 + (COALESCE(del.quality_pass_rate, 90.0) * 0.25) + ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 88 THEN 'Tier 1 - Strategic Partner'
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) + 25.0 + (COALESCE(del.quality_pass_rate, 90.0) * 0.25) + ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 75 THEN 'Tier 2 - Preferred Supplier'
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) + 25.0 + (COALESCE(del.quality_pass_rate, 90.0) * 0.25) + ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 60 THEN 'Tier 3 - Operational Supplier'
        ELSE 'Tier 4 - High Risk / PIP Required'
    END AS vendor_performance_tier,
    CURRENT_TIMESTAMP AS dbt_updated_at
FROM {{ ref('stg_vendors') }} v
LEFT JOIN vendor_po_stats pos ON v.vendor_id = pos.vendor_id
LEFT JOIN vendor_delivery_stats del ON v.vendor_id = del.vendor_id
LEFT JOIN vendor_compliance_stats comp ON v.vendor_id = comp.vendor_id
