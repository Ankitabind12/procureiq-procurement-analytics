-- =============================================================================
-- ProcureIQ Data Warehouse: Silver Layer Transformations
-- Cleans, deduplicates, validates integrity, standardizes types & normalizes
-- =============================================================================

-- 1. Silver Departments
CREATE TABLE IF NOT EXISTS silver_departments AS
SELECT DISTINCT
    TRIM(department_id) AS department_id,
    TRIM(department_name) AS department_name,
    UPPER(TRIM(cost_center)) AS cost_center,
    CAST(annual_budget AS NUMERIC(15, 2)) AS annual_budget,
    TRIM(manager) AS manager,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_departments
WHERE department_id IS NOT NULL;

-- 2. Silver Categories
CREATE TABLE IF NOT EXISTS silver_categories AS
SELECT DISTINCT
    TRIM(category_id) AS category_id,
    TRIM(category_name) AS category_name,
    TRIM(spend_tier) AS spend_tier,
    TRIM(description) AS description,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_categories
WHERE category_id IS NOT NULL;

-- 3. Silver Products
CREATE TABLE IF NOT EXISTS silver_products AS
SELECT DISTINCT
    TRIM(product_id) AS product_id,
    TRIM(product_name) AS product_name,
    TRIM(category_id) AS category_id,
    CAST(standard_cost AS NUMERIC(12, 2)) AS standard_cost,
    TRIM(uom) AS uom,
    CAST(created_date AS DATE) AS created_date,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_products
WHERE product_id IS NOT NULL AND standard_cost > 0;

-- 4. Silver Date Dimension
CREATE TABLE IF NOT EXISTS silver_date_dimension AS
SELECT DISTINCT
    CAST(date_key AS INTEGER) AS date_key,
    CAST(full_date AS DATE) AS full_date,
    CAST(year AS INTEGER) AS year,
    TRIM(quarter) AS quarter,
    CAST(month AS INTEGER) AS month,
    TRIM(month_name) AS month_name,
    CAST(day AS INTEGER) AS day,
    TRIM(day_of_week) AS day_of_week,
    is_weekend,
    CAST(fiscal_year AS INTEGER) AS fiscal_year,
    TRIM(fiscal_quarter) AS fiscal_quarter,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_date_dimension
WHERE date_key IS NOT NULL;

-- 5. Silver Vendors
CREATE TABLE IF NOT EXISTS silver_vendors AS
SELECT DISTINCT
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
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_vendors
WHERE vendor_id IS NOT NULL;

-- 6. Silver Vendor Compliance
CREATE TABLE IF NOT EXISTS silver_vendor_compliance AS
SELECT DISTINCT
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
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_vendor_compliance
WHERE compliance_id IS NOT NULL;

-- 7. Silver Purchase Orders
CREATE TABLE IF NOT EXISTS silver_purchase_orders AS
SELECT DISTINCT
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    TRIM(department_id) AS department_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(promised_delivery_date AS DATE) AS promised_delivery_date,
    TRIM(po_status) AS po_status,
    TRIM(currency) AS currency,
    CAST(total_po_amount AS NUMERIC(15, 2)) AS total_po_amount,
    TRIM(buyer_name) AS buyer_name,
    CASE 
        WHEN po_status = 'Fulfilled' THEN 1
        ELSE 0
    END AS is_fulfilled,
    CASE 
        WHEN po_status = 'Cancelled' THEN 1
        ELSE 0
    END AS is_cancelled,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_purchase_orders
WHERE po_id IS NOT NULL;

-- 8. Silver Purchase Order Items
CREATE TABLE IF NOT EXISTS silver_purchase_order_items AS
SELECT DISTINCT
    TRIM(line_item_id) AS line_item_id,
    TRIM(po_id) AS po_id,
    CAST(line_number AS INTEGER) AS line_number,
    TRIM(product_id) AS product_id,
    CAST(quantity_ordered AS INTEGER) AS quantity_ordered,
    CAST(unit_price AS NUMERIC(12, 2)) AS unit_price,
    CAST(line_total_amount AS NUMERIC(15, 2)) AS line_total_amount,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_purchase_order_items
WHERE line_item_id IS NOT NULL AND quantity_ordered > 0;

-- 9. Silver Deliveries
CREATE TABLE IF NOT EXISTS silver_deliveries AS
SELECT DISTINCT
    TRIM(delivery_id) AS delivery_id,
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    CAST(promised_delivery_date AS DATE) AS promised_delivery_date,
    CAST(actual_delivery_date AS DATE) AS actual_delivery_date,
    CAST(delay_days AS INTEGER) AS delay_days,
    TRIM(delivery_status) AS delivery_status,
    CASE 
        WHEN CAST(delay_days AS INTEGER) <= 0 THEN 1 
        ELSE 0 
    END AS is_ontime,
    CASE 
        WHEN CAST(delay_days AS INTEGER) <= 0 THEN '0. On-Time'
        WHEN CAST(delay_days AS INTEGER) BETWEEN 1 AND 7 THEN '1. 1-7 Days Delay'
        WHEN CAST(delay_days AS INTEGER) BETWEEN 8 AND 14 THEN '2. 8-14 Days Delay'
        ELSE '3. 15+ Days Severe Delay'
    END AS delay_bucket,
    TRIM(quality_inspection_result) AS quality_inspection_result,
    CASE 
        WHEN TRIM(quality_inspection_result) = 'Pass' THEN 1 
        ELSE 0 
    END AS is_quality_pass,
    CAST(defect_rate_percentage AS NUMERIC(6, 2)) AS defect_rate_percentage,
    TRIM(carrier_name) AS carrier_name,
    TRIM(tracking_number) AS tracking_number,
    TRIM(received_by) AS received_by,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_deliveries
WHERE delivery_id IS NOT NULL;

-- 10. Silver Invoices
CREATE TABLE IF NOT EXISTS silver_invoices AS
SELECT DISTINCT
    TRIM(invoice_id) AS invoice_id,
    TRIM(po_id) AS po_id,
    TRIM(vendor_id) AS vendor_id,
    CAST(invoice_date AS DATE) AS invoice_date,
    CAST(payment_due_date AS DATE) AS payment_due_date,
    CAST(po_amount AS NUMERIC(15, 2)) AS po_amount,
    CAST(invoice_amount AS NUMERIC(15, 2)) AS invoice_amount,
    CAST(discrepancy_amount AS NUMERIC(15, 2)) AS discrepancy_amount,
    is_discrepancy,
    TRIM(discrepancy_reason) AS discrepancy_reason,
    ROUND(CAST(discrepancy_amount AS NUMERIC) / NULLIF(CAST(po_amount AS NUMERIC), 0) * 100.0, 2) AS discrepancy_percentage,
    CASE 
        WHEN is_discrepancy = true AND discrepancy_amount > 0 THEN 'OVERBILLING_LEAKAGE'
        WHEN is_discrepancy = true AND discrepancy_amount < 0 THEN 'UNDERBILLING'
        ELSE 'ACCURATE_MATCH'
    END AS audit_reconciliation_category,
    TRIM(payment_status) AS payment_status,
    TRIM(currency) AS currency,
    CURRENT_TIMESTAMP AS _silver_processed_at
FROM bronze_invoices
WHERE invoice_id IS NOT NULL;
