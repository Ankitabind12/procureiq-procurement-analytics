-- =============================================================================
-- ProcureIQ Data Warehouse: Star Schema Dimension and Fact Views
-- =============================================================================

-- DIMENSION 1: dim_vendor
CREATE VIEW IF NOT EXISTS dim_vendor AS
SELECT 
    v.vendor_id,
    v.vendor_name,
    v.primary_category_id,
    c.category_name AS primary_category_name,
    v.country,
    v.city,
    v.payment_terms,
    v.risk_rating,
    v.vendor_status,
    v.registration_date
FROM silver_vendors v
LEFT JOIN silver_categories c ON v.primary_category_id = c.category_id;

-- DIMENSION 2: dim_product
CREATE VIEW IF NOT EXISTS dim_product AS
SELECT 
    p.product_id,
    p.product_name,
    p.category_id,
    c.category_name,
    p.standard_cost,
    p.uom,
    p.created_date
FROM silver_products p
LEFT JOIN silver_categories c ON p.category_id = c.category_id;

-- DIMENSION 3: dim_department
CREATE VIEW IF NOT EXISTS dim_department AS
SELECT 
    department_id,
    department_name,
    cost_center,
    annual_budget,
    manager
FROM silver_departments;

-- DIMENSION 4: dim_date
CREATE VIEW IF NOT EXISTS dim_date AS
SELECT 
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    day,
    day_of_week,
    is_weekend,
    fiscal_year,
    fiscal_quarter
FROM silver_date_dimension;

-- DIMENSION 5: dim_category
CREATE VIEW IF NOT EXISTS dim_category AS
SELECT 
    category_id,
    category_name,
    spend_tier,
    description
FROM silver_categories;

-- FACT 1: fact_purchase_orders (Grain: One row per PO Line Item)
CREATE VIEW IF NOT EXISTS fact_purchase_orders AS
SELECT 
    poi.line_item_id,
    po.po_id,
    po.vendor_id,
    po.department_id,
    poi.product_id,
    po.order_date,
    CAST(REPLACE(CAST(po.order_date AS VARCHAR), '-', '') AS INTEGER) AS order_date_key,
    po.promised_delivery_date,
    CAST(REPLACE(CAST(po.promised_delivery_date AS VARCHAR), '-', '') AS INTEGER) AS promised_date_key,
    po.po_status,
    po.buyer_name,
    poi.line_number,
    poi.quantity_ordered,
    poi.unit_price,
    poi.line_total_amount,
    po.total_po_amount AS po_header_total,
    po.is_fulfilled,
    po.is_cancelled
FROM silver_purchase_order_items poi
JOIN silver_purchase_orders po ON poi.po_id = po.po_id;

-- FACT 2: fact_deliveries (Grain: One row per delivery shipment)
CREATE VIEW IF NOT EXISTS fact_deliveries AS
SELECT 
    d.delivery_id,
    d.po_id,
    d.vendor_id,
    d.promised_delivery_date,
    d.actual_delivery_date,
    CAST(REPLACE(CAST(d.actual_delivery_date AS VARCHAR), '-', '') AS INTEGER) AS actual_delivery_date_key,
    d.delay_days,
    d.delivery_status,
    d.is_ontime,
    d.delay_bucket,
    d.quality_inspection_result,
    d.is_quality_pass,
    d.defect_rate_percentage,
    d.carrier_name,
    d.tracking_number
FROM silver_deliveries d;

-- FACT 3: fact_invoices (Grain: One row per vendor invoice)
CREATE VIEW IF NOT EXISTS fact_invoices AS
SELECT 
    inv.invoice_id,
    inv.po_id,
    inv.vendor_id,
    inv.invoice_date,
    CAST(REPLACE(CAST(inv.invoice_date AS VARCHAR), '-', '') AS INTEGER) AS invoice_date_key,
    inv.payment_due_date,
    inv.po_amount,
    inv.invoice_amount,
    inv.discrepancy_amount,
    inv.is_discrepancy,
    inv.discrepancy_reason,
    inv.discrepancy_percentage,
    inv.audit_reconciliation_category,
    inv.payment_status
FROM silver_invoices inv;
