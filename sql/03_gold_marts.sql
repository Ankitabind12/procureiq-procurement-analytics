-- =============================================================================
-- ProcureIQ Data Warehouse: Gold Layer Business Marts
-- Enterprise analytical tables with business scoring, spend aggregations,
-- and multi-pillar vendor performance evaluations
-- =============================================================================

-- 1. Gold Vendor Scorecard
CREATE TABLE IF NOT EXISTS gold_vendor_scorecard AS
WITH vendor_po_stats AS (
    SELECT 
        po.vendor_id,
        COUNT(po.po_id) AS total_orders,
        SUM(po.total_po_amount) AS total_spend,
        SUM(po.is_fulfilled) AS fulfilled_orders,
        SUM(po.is_cancelled) AS cancelled_orders,
        ROUND(CAST(SUM(po.is_fulfilled) AS NUMERIC) / NULLIF(COUNT(po.po_id), 0) * 100.0, 2) AS po_fulfilment_rate
    FROM silver_purchase_orders po
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
    FROM silver_deliveries d
    GROUP BY d.vendor_id
),
vendor_compliance_stats AS (
    SELECT 
        c.vendor_id,
        COUNT(c.compliance_id) AS total_certs,
        ROUND(AVG(c.audit_score), 2) AS avg_audit_score,
        SUM(CASE WHEN c.compliance_risk_tier = 'HIGH RISK - EXPIRED' THEN 1 ELSE 0 END) AS expired_certs_count
    FROM silver_vendor_compliance c
    GROUP BY c.vendor_id
),
vendor_price_stats AS (
    SELECT 
        po.vendor_id,
        ROUND(AVG(poi.unit_price / NULLIF(p.standard_cost, 0)), 4) AS price_index_ratio
    FROM silver_purchase_orders po
    JOIN silver_purchase_order_items poi ON po.po_id = poi.po_id
    JOIN silver_products p ON poi.product_id = p.product_id
    GROUP BY po.vendor_id
)
SELECT 
    v.vendor_id,
    v.vendor_name,
    c.category_name AS primary_category,
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
    COALESCE(prc.price_index_ratio, 1.0) AS price_index_ratio,
    
    -- 4-Pillar Transparent Scoring (Delivery 35%, Price 25%, Quality 25%, Compliance 15%)
    ROUND(COALESCE(del.ontime_delivery_rate, 85.0) * 0.35, 2) AS delivery_reliability_score,
    ROUND(GREATEST(0, (2.0 - COALESCE(prc.price_index_ratio, 1.0)) * 100.0 * 0.25), 2) AS price_competitiveness_score,
    ROUND(COALESCE(del.quality_pass_rate, 90.0) * 0.25, 2) AS product_quality_score,
    ROUND((COALESCE(comp.avg_audit_score, 80.0)) * 0.15, 2) AS compliance_score,
    
    -- Composite Vendor Performance Score (Out of 100)
    ROUND(
        (COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) +
        (GREATEST(0, (2.0 - COALESCE(prc.price_index_ratio, 1.0)) * 100.0 * 0.25)) +
        (COALESCE(del.quality_pass_rate, 90.0) * 0.25) +
        ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15),
        2
    ) AS composite_performance_score,
    
    -- Performance Tier Classification
    CASE 
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) +
              (GREATEST(0, (2.0 - COALESCE(prc.price_index_ratio, 1.0)) * 100.0 * 0.25)) +
              (COALESCE(del.quality_pass_rate, 90.0) * 0.25) +
              ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 88 THEN 'Tier 1 - Strategic Partner'
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) +
              (GREATEST(0, (2.0 - COALESCE(prc.price_index_ratio, 1.0)) * 100.0 * 0.25)) +
              (COALESCE(del.quality_pass_rate, 90.0) * 0.25) +
              ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 75 THEN 'Tier 2 - Preferred Supplier'
        WHEN ((COALESCE(del.ontime_delivery_rate, 85.0) * 0.35) +
              (GREATEST(0, (2.0 - COALESCE(prc.price_index_ratio, 1.0)) * 100.0 * 0.25)) +
              (COALESCE(del.quality_pass_rate, 90.0) * 0.25) +
              ((COALESCE(comp.avg_audit_score, 80.0)) * 0.15)) >= 60 THEN 'Tier 3 - Operational Supplier'
        ELSE 'Tier 4 - High Risk / PIP Required'
    END AS vendor_performance_tier,
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_vendors v
LEFT JOIN silver_categories c ON v.primary_category_id = c.category_id
LEFT JOIN vendor_po_stats pos ON v.vendor_id = pos.vendor_id
LEFT JOIN vendor_delivery_stats del ON v.vendor_id = del.vendor_id
LEFT JOIN vendor_compliance_stats comp ON v.vendor_id = comp.vendor_id
LEFT JOIN vendor_price_stats prc ON v.vendor_id = prc.vendor_id;

-- 2. Gold Procurement Spend
CREATE TABLE IF NOT EXISTS gold_procurement_spend AS
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
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_purchase_orders po
JOIN silver_date_dimension d ON po.order_date = d.full_date
JOIN silver_departments dept ON po.department_id = dept.department_id
JOIN silver_vendors v ON po.vendor_id = v.vendor_id
JOIN silver_categories cat ON v.primary_category_id = cat.category_id
GROUP BY d.year, d.quarter, d.month, d.month_name, dept.department_name, dept.cost_center, cat.category_name, cat.spend_tier;

-- 3. Gold Delivery Performance
CREATE TABLE IF NOT EXISTS gold_delivery_performance AS
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
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_deliveries d
JOIN silver_vendors v ON d.vendor_id = v.vendor_id
JOIN silver_categories cat ON v.primary_category_id = cat.category_id
GROUP BY v.vendor_id, v.vendor_name, cat.category_name, d.carrier_name, d.delay_bucket;

-- 4. Gold Invoice Analysis
CREATE TABLE IF NOT EXISTS gold_invoice_analysis AS
SELECT 
    v.vendor_id,
    v.vendor_name,
    cat.category_name,
    inv.discrepancy_reason,
    inv.audit_reconciliation_category,
    COUNT(inv.invoice_id) AS total_invoices_count,
    SUM(inv.po_amount) AS total_po_baseline_amount,
    SUM(inv.invoice_amount) AS total_billed_amount,
    SUM(inv.discrepancy_amount) AS total_discrepancy_leakage,
    ROUND(AVG(inv.discrepancy_percentage), 2) AS avg_discrepancy_percentage,
    SUM(CASE WHEN inv.is_discrepancy = true THEN 1 ELSE 0 END) AS discrepant_invoices_count,
    SUM(CASE WHEN inv.payment_status = 'Disputed' THEN 1 ELSE 0 END) AS disputed_invoices_count,
    SUM(CASE WHEN inv.payment_status = 'Paid' THEN 1 ELSE 0 END) AS paid_invoices_count,
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_invoices inv
JOIN silver_vendors v ON inv.vendor_id = v.vendor_id
JOIN silver_categories cat ON v.primary_category_id = cat.category_id
GROUP BY v.vendor_id, v.vendor_name, cat.category_name, inv.discrepancy_reason, inv.audit_reconciliation_category;

-- 5. Gold Compliance Status
CREATE TABLE IF NOT EXISTS gold_compliance_status AS
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
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_vendor_compliance c
JOIN silver_vendors v ON c.vendor_id = v.vendor_id
JOIN silver_categories cat ON v.primary_category_id = cat.category_id;

-- 6. Gold Purchase Order Summary
CREATE TABLE IF NOT EXISTS gold_purchase_order_summary AS
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
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_purchase_orders po
JOIN silver_vendors v ON po.vendor_id = v.vendor_id
JOIN silver_departments dept ON po.department_id = dept.department_id
LEFT JOIN silver_purchase_order_items poi ON po.po_id = poi.po_id
GROUP BY po.po_id, v.vendor_name, dept.department_name, po.order_date, po.promised_delivery_date, po.po_status, po.total_po_amount, po.buyer_name, po.is_fulfilled, po.is_cancelled;

-- 7. Gold Category Performance
CREATE TABLE IF NOT EXISTS gold_category_performance AS
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
    CURRENT_TIMESTAMP AS _gold_updated_at
FROM silver_categories cat
JOIN silver_vendors v ON cat.category_id = v.primary_category_id
JOIN silver_purchase_orders po ON v.vendor_id = po.vendor_id
JOIN silver_purchase_order_items poi ON po.po_id = poi.po_id
GROUP BY cat.category_id, cat.category_name, cat.spend_tier;
