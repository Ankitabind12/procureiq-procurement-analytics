-- =============================================================================
-- ProcureIQ: Executive Business Analyst Analytical Queries
-- Real-world SQL queries used by Business Analysts and Procurement Leaders
-- =============================================================================

-- QUERY 1: Executive KPI Dashboard Summary
-- Calculates high-level procurement metrics in a single view
SELECT 
    COUNT(DISTINCT po.po_id) AS total_purchase_orders,
    ROUND(SUM(po.total_po_amount), 2) AS total_procurement_spend,
    ROUND(AVG(po.total_po_amount), 2) AS avg_po_amount,
    COUNT(DISTINCT po.vendor_id) AS active_vendors_count,
    ROUND(CAST(SUM(po.is_fulfilled) AS NUMERIC) / NULLIF(COUNT(po.po_id), 0) * 100.0, 2) AS po_fulfilment_rate_pct,
    ROUND(CAST(SUM(po.is_cancelled) AS NUMERIC) / NULLIF(COUNT(po.po_id), 0) * 100.0, 2) AS po_cancellation_rate_pct,
    ROUND(CAST(SUM(d.is_ontime) AS NUMERIC) / NULLIF(COUNT(d.delivery_id), 0) * 100.0, 2) AS overall_ontime_delivery_rate_pct,
    ROUND(AVG(d.delay_days), 2) AS avg_delivery_delay_days,
    ROUND(CAST(SUM(CASE WHEN inv.is_discrepancy = true THEN 1 ELSE 0 END) AS NUMERIC) / NULLIF(COUNT(inv.invoice_id), 0) * 100.0, 2) AS invoice_discrepancy_rate_pct,
    ROUND(SUM(inv.discrepancy_amount), 2) AS total_invoice_discrepancy_leakage
FROM silver_purchase_orders po
LEFT JOIN silver_deliveries d ON po.po_id = d.po_id
LEFT JOIN silver_invoices inv ON po.po_id = inv.po_id;

-- QUERY 2: Top 10 Worst Vendors by Average Delivery Delay
SELECT 
    v.vendor_id,
    v.vendor_name,
    c.category_name,
    COUNT(d.delivery_id) AS total_deliveries,
    ROUND(AVG(d.delay_days), 2) AS avg_delay_days,
    ROUND(CAST(SUM(d.is_ontime) AS NUMERIC) / COUNT(d.delivery_id) * 100.0, 2) AS ontime_pct,
    ROUND(SUM(po.total_po_amount), 2) AS total_spend_exposure
FROM silver_deliveries d
JOIN silver_vendors v ON d.vendor_id = v.vendor_id
JOIN silver_categories c ON v.primary_category_id = c.category_id
JOIN silver_purchase_orders po ON d.po_id = po.po_id
GROUP BY v.vendor_id, v.vendor_name, c.category_name
HAVING COUNT(d.delivery_id) >= 5
ORDER BY avg_delay_days DESC
LIMIT 10;

-- QUERY 3: Invoice Leakage & Discrepancy Breakdown by Reason
SELECT 
    inv.discrepancy_reason,
    COUNT(inv.invoice_id) AS invoice_count,
    ROUND(SUM(inv.po_amount), 2) AS total_po_amount,
    ROUND(SUM(inv.invoice_amount), 2) AS total_billed_amount,
    ROUND(SUM(inv.discrepancy_amount), 2) AS total_leakage_dollars,
    ROUND(AVG(inv.discrepancy_percentage), 2) AS avg_discrepancy_pct
FROM silver_invoices inv
GROUP BY inv.discrepancy_reason
ORDER BY total_leakage_dollars DESC;

-- QUERY 4: Compliance Risk Audit: Non-Compliant Vendors Receiving Orders
SELECT 
    v.vendor_id,
    v.vendor_name,
    vc.document_type,
    vc.expiry_date,
    vc.compliance_risk_tier,
    COUNT(po.po_id) AS open_or_fulfilled_pos,
    ROUND(SUM(po.total_po_amount), 2) AS committed_spend
FROM silver_vendor_compliance vc
JOIN silver_vendors v ON vc.vendor_id = v.vendor_id
JOIN silver_purchase_orders po ON v.vendor_id = po.vendor_id
WHERE vc.compliance_risk_tier = 'HIGH RISK - EXPIRED'
GROUP BY v.vendor_id, v.vendor_name, vc.document_type, vc.expiry_date, vc.compliance_risk_tier
ORDER BY committed_spend DESC
LIMIT 15;

-- QUERY 5: Category Spend Dispersion & Unit Price Variance
SELECT 
    cat.category_name,
    COUNT(DISTINCT poi.product_id) AS distinct_products,
    COUNT(poi.line_item_id) AS total_order_lines,
    ROUND(SUM(poi.line_total_amount), 2) AS total_category_spend,
    ROUND(AVG(poi.unit_price), 2) AS avg_paid_unit_price,
    ROUND(MIN(poi.unit_price), 2) AS min_paid_unit_price,
    ROUND(MAX(poi.unit_price), 2) AS max_paid_unit_price
FROM silver_purchase_order_items poi
JOIN silver_products p ON poi.product_id = p.product_id
JOIN silver_categories cat ON p.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_category_spend DESC;

-- QUERY 6: Vendor Tier Distribution and Strategic Classification
SELECT 
    vendor_performance_tier,
    COUNT(vendor_id) AS vendor_count,
    ROUND(COUNT(vendor_id) * 100.0 / (SELECT COUNT(*) FROM gold_vendor_scorecard), 2) AS vendor_share_pct,
    ROUND(SUM(total_spend), 2) AS total_tier_spend,
    ROUND(AVG(composite_performance_score), 2) AS avg_composite_score,
    ROUND(AVG(ontime_delivery_rate), 2) AS avg_ontime_rate_pct,
    ROUND(AVG(quality_pass_rate), 2) AS avg_quality_pass_pct
FROM gold_vendor_scorecard
GROUP BY vendor_performance_tier
ORDER BY avg_composite_score DESC;
