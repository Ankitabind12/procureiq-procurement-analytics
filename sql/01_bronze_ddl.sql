-- =============================================================================
-- ProcureIQ Data Warehouse: Bronze Layer DDL (Raw Ingestion)
-- Preserves source fidelity with operational audit metadata
-- =============================================================================

-- 1. Bronze Departments
CREATE TABLE IF NOT EXISTS bronze_departments (
    department_id VARCHAR(32),
    department_name VARCHAR(128),
    cost_center VARCHAR(64),
    annual_budget NUMERIC(15, 2),
    manager VARCHAR(128),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 2. Bronze Categories
CREATE TABLE IF NOT EXISTS bronze_categories (
    category_id VARCHAR(32),
    category_name VARCHAR(128),
    spend_tier VARCHAR(64),
    description TEXT,
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 3. Bronze Products
CREATE TABLE IF NOT EXISTS bronze_products (
    product_id VARCHAR(32),
    product_name VARCHAR(255),
    category_id VARCHAR(32),
    standard_cost NUMERIC(12, 2),
    uom VARCHAR(64),
    created_date VARCHAR(32),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 4. Bronze Date Dimension
CREATE TABLE IF NOT EXISTS bronze_date_dimension (
    date_key INTEGER,
    full_date VARCHAR(32),
    year INTEGER,
    quarter VARCHAR(16),
    month INTEGER,
    month_name VARCHAR(32),
    day INTEGER,
    day_of_week VARCHAR(32),
    is_weekend BOOLEAN,
    fiscal_year INTEGER,
    fiscal_quarter VARCHAR(16),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 5. Bronze Vendors
CREATE TABLE IF NOT EXISTS bronze_vendors (
    vendor_id VARCHAR(32),
    vendor_name VARCHAR(255),
    primary_category_id VARCHAR(32),
    country VARCHAR(64),
    city VARCHAR(64),
    contact_email VARCHAR(128),
    payment_terms VARCHAR(32),
    risk_rating VARCHAR(32),
    vendor_status VARCHAR(32),
    registration_date VARCHAR(32),
    delivery_reliability_bias NUMERIC(6, 4),
    price_competitiveness_bias NUMERIC(6, 4),
    quality_defect_rate_bias NUMERIC(6, 4),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 6. Bronze Vendor Compliance
CREATE TABLE IF NOT EXISTS bronze_vendor_compliance (
    compliance_id VARCHAR(32),
    vendor_id VARCHAR(32),
    document_type VARCHAR(128),
    issue_date VARCHAR(32),
    expiry_date VARCHAR(32),
    compliance_status VARCHAR(64),
    audit_score INTEGER,
    auditor_name VARCHAR(128),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 7. Bronze Purchase Orders
CREATE TABLE IF NOT EXISTS bronze_purchase_orders (
    po_id VARCHAR(32),
    vendor_id VARCHAR(32),
    department_id VARCHAR(32),
    order_date VARCHAR(32),
    promised_delivery_date VARCHAR(32),
    po_status VARCHAR(32),
    currency VARCHAR(16),
    total_po_amount NUMERIC(15, 2),
    buyer_name VARCHAR(128),
    created_at VARCHAR(32),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 8. Bronze Purchase Order Items
CREATE TABLE IF NOT EXISTS bronze_purchase_order_items (
    line_item_id VARCHAR(32),
    po_id VARCHAR(32),
    line_number INTEGER,
    product_id VARCHAR(32),
    quantity_ordered INTEGER,
    unit_price NUMERIC(12, 2),
    line_total_amount NUMERIC(15, 2),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 9. Bronze Deliveries
CREATE TABLE IF NOT EXISTS bronze_deliveries (
    delivery_id VARCHAR(32),
    po_id VARCHAR(32),
    vendor_id VARCHAR(32),
    promised_delivery_date VARCHAR(32),
    actual_delivery_date VARCHAR(32),
    delay_days INTEGER,
    delivery_status VARCHAR(32),
    quality_inspection_result VARCHAR(64),
    defect_rate_percentage NUMERIC(6, 2),
    carrier_name VARCHAR(128),
    tracking_number VARCHAR(64),
    received_by VARCHAR(128),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);

-- 10. Bronze Invoices
CREATE TABLE IF NOT EXISTS bronze_invoices (
    invoice_id VARCHAR(32),
    po_id VARCHAR(32),
    vendor_id VARCHAR(32),
    invoice_date VARCHAR(32),
    payment_due_date VARCHAR(32),
    po_amount NUMERIC(15, 2),
    invoice_amount NUMERIC(15, 2),
    discrepancy_amount NUMERIC(15, 2),
    is_discrepancy BOOLEAN,
    discrepancy_reason VARCHAR(64),
    payment_status VARCHAR(32),
    currency VARCHAR(16),
    data_source_type VARCHAR(64),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _source_file VARCHAR(255),
    _batch_id VARCHAR(64)
);
