# ProcureIQ: Gold Layer Data Dictionary

This document details the schema, column definitions, data types, and business semantics of all seven certified Gold Analytical Marts in the ProcureIQ Data Warehouse.

---

### 1. `gold_vendor_scorecard`
**Description**: Consolidated 360-degree supplier performance scorecard integrating delivery reliability, quality pass rates, price competitiveness, and compliance scores.  
**Granularity**: Exactly one row per vendor.

| Column Name | Data Type | Nullable | Description / Calculation | Sample Value |
|---|---|---|---|---|
| `vendor_id` | VARCHAR(32) | NO | Unique primary identifier for vendor. | `VND-0001` |
| `vendor_name` | VARCHAR(255) | NO | Legal business name. | `Apex Industrial Group` |
| `primary_category` | VARCHAR(128) | YES | Primary sourcing commodity category. | `Raw Industrial Materials` |
| `country` | VARCHAR(64) | YES | Country of supplier headquarters. | `USA` |
| `city` | VARCHAR(64) | YES | Operating city. | `Chicago` |
| `payment_terms` | VARCHAR(32) | YES | Agreed credit terms. | `Net 30` |
| `risk_rating` | VARCHAR(32) | YES | Baseline operational risk rating (`Low`, `Medium`, `High`). | `Low` |
| `vendor_status` | VARCHAR(32) | YES | Supplier administrative status (`Active`, `Suspended`). | `Active` |
| `total_orders` | BIGINT | NO | Total number of purchase orders awarded to vendor. | `14` |
| `total_spend` | NUMERIC(15, 2) | NO | Aggregate spend committed to vendor ($). | `1542100.50` |
| `po_fulfilment_rate` | NUMERIC(5, 2) | YES | Percentage of POs successfully fulfilled. | `78.57` |
| `cancelled_orders` | BIGINT | NO | Number of cancelled purchase orders. | `1` |
| `total_deliveries` | BIGINT | NO | Total receiving shipments processed. | `10` |
| `ontime_delivery_rate` | NUMERIC(5, 2) | YES | Percentage of deliveries arriving &le; promised date. | `90.00` |
| `avg_delay_days` | NUMERIC(6, 2) | YES | Average calendar delay days. | `0.45` |
| `quality_pass_rate` | NUMERIC(5, 2) | YES | Percentage of shipments passing dock QC inspection. | `95.00` |
| `avg_compliance_score`| NUMERIC(5, 2) | YES | Average compliance audit score across all certificates. | `88.50` |
| `expired_certs_count` | BIGINT | NO | Count of expired compliance documents currently on file. | `0` |
| `delivery_reliability_score` | NUMERIC(5, 2) | YES | Weighted delivery score component (35% weight). | `31.50` |
| `price_competitiveness_score`| NUMERIC(5, 2) | YES | Weighted price score component (25% weight). | `25.00` |
| `product_quality_score` | NUMERIC(5, 2) | YES | Weighted quality score component (25% weight). | `23.75` |
| `compliance_score` | NUMERIC(5, 2) | YES | Weighted compliance score component (15% weight). | `13.28` |
| `composite_performance_score` | NUMERIC(5, 2) | YES | Composite 0-100 vendor rating. | `93.53` |
| `vendor_performance_tier` | VARCHAR(64) | YES | Performance tier (`Tier 1 - Strategic Partner`, `Tier 2`, `Tier 3`, `Tier 4 - PIP`). | `Tier 1 - Strategic Partner` |

---

### 2. `gold_procurement_spend`
**Description**: Temporal spend aggregates across departments, cost centers, and commodity categories.  
**Granularity**: One row per Year, Quarter, Month, Department, and Category.

| Column Name | Data Type | Description |
|---|---|---|
| `year` | INTEGER | Calendar year of purchase order placement (e.g., `2024`). |
| `quarter` | VARCHAR(16) | Calendar quarter (e.g., `Q3`). |
| `month` | INTEGER | Calendar month number (`1` to `12`). |
| `month_name` | VARCHAR(32) | Calendar month name (e.g., `October`). |
| `department_name` | VARCHAR(128) | Procuring business department. |
| `cost_center` | VARCHAR(64) | Cost center code (e.g., `CC-101`). |
| `category_name` | VARCHAR(128) | Procurement category. |
| `spend_tier` | VARCHAR(64) | Strategic criticality tier (`Tier 1 - Strategic`, `Tier 2 - Operational`). |
| `total_po_count` | BIGINT | Count of distinct POs placed in this partition. |
| `total_spend` | NUMERIC(15, 2) | Aggregate dollar spend in this partition. |
| `avg_po_amount` | NUMERIC(15, 2) | Mean PO dollar value. |
| `fulfilled_spend` | NUMERIC(15, 2) | Spend associated with successfully fulfilled POs. |
| `cancelled_spend` | NUMERIC(15, 2) | Spend associated with cancelled POs. |

---

### 3. `gold_delivery_performance`
**Description**: Logistics carrier and supplier delivery reliability analysis.  
**Granularity**: One row per Vendor, Category, Carrier, and Delay Bucket.

| Column Name | Data Type | Description |
|---|---|---|
| `vendor_id` | VARCHAR(32) | Unique Vendor ID. |
| `vendor_name` | VARCHAR(255) | Vendor name. |
| `category_name` | VARCHAR(128) | Product category shipped. |
| `carrier_name` | VARCHAR(128) | Freight carrier (e.g., `FedEx Freight`, `DHL`). |
| `delay_bucket` | VARCHAR(64) | Delay tier (`0. On-Time`, `1. 1-7 Days Delay`, `2. 8-14 Days Delay`, `3. 15+ Days Severe Delay`). |
| `shipment_count` | BIGINT | Number of shipments in this group. |
| `ontime_count` | BIGINT | Number of on-time shipments. |
| `delayed_count` | BIGINT | Number of delayed shipments. |
| `ontime_percentage` | NUMERIC(5, 2) | On-time delivery percentage (%). |
| `avg_delay_days` | NUMERIC(6, 2) | Average days delayed past SLA. |
| `quality_passed_count` | BIGINT | Shipments passing quality inspection. |
| `quality_pass_percentage` | NUMERIC(5, 2) | QC pass rate (%). |
| `avg_defect_percentage` | NUMERIC(6, 2) | Mean defect percentage identified during inspection. |

---

### 4. `gold_invoice_analysis`
**Description**: Accounts Payable 3-way match reconciliation and overbilling leakage analysis.  
**Granularity**: One row per Vendor, Category, Discrepancy Reason, and Audit Category.

| Column Name | Data Type | Description |
|---|---|---|
| `vendor_id` | VARCHAR(32) | Unique Vendor ID. |
| `vendor_name` | VARCHAR(255) | Vendor business name. |
| `category_name` | VARCHAR(128) | Primary category. |
| `discrepancy_reason` | VARCHAR(64) | Root cause (`No Discrepancy`, `Price Discrepancy`, `Quantity Discrepancy`, `Severe Variance`). |
| `audit_reconciliation_category` | VARCHAR(64) | AP classification (`ACCURATE_MATCH`, `OVERBILLING_LEAKAGE`, `UNDERBILLING`). |
| `total_invoices_count` | BIGINT | Count of invoices evaluated. |
| `total_po_baseline_amount` | NUMERIC(15, 2) | Expected amount based on approved PO. |
| `total_billed_amount` | NUMERIC(15, 2) | Actual gross amount billed on invoices. |
| `total_discrepancy_leakage` | NUMERIC(15, 2) | Variance amount ($ billed minus $ PO baseline). |
| `avg_discrepancy_percentage` | NUMERIC(5, 2) | Mean percentage variance. |
| `discrepant_invoices_count` | BIGINT | Count of non-matching invoices. |
| `disputed_invoices_count` | BIGINT | Count of invoices currently in formal dispute status. |
| `paid_invoices_count` | BIGINT | Count of settled invoices. |

---

### 5. `gold_compliance_status`
**Description**: Regulatory, environmental, and liability insurance audit log with real-time risk tiers.  
**Granularity**: One row per compliance certificate.

| Column Name | Data Type | Description |
|---|---|---|
| `compliance_id` | VARCHAR(32) | Unique certificate record ID. |
| `vendor_id` | VARCHAR(32) | Associated Vendor ID. |
| `vendor_name` | VARCHAR(255) | Vendor business name. |
| `document_type` | VARCHAR(128) | Certificate name (e.g., `ISO 9001`, `Commercial Insurance`). |
| `issue_date` | DATE | Date certificate was issued. |
| `expiry_date` | DATE | Expiration date of certificate. |
| `compliance_status` | VARCHAR(64) | Status (`Compliant`, `Expired`, `Pending Renewal`). |
| `compliance_risk_tier` | VARCHAR(64) | Automated risk classification (`HIGH RISK - EXPIRED`, `MEDIUM RISK - EXPIRING SOON`, `LOW RISK - VALID`). |
| `audit_score` | INTEGER | Third-party compliance audit score (0 to 100). |
| `auditor_name` | VARCHAR(128) | Auditing agency (e.g., `TÜV SÜD`, `Bureau Veritas`). |
| `action_recommendation` | TEXT | Automated recommendation (`Immediate Stop-Shipment`, `Notify Vendor`). |

---

### 6. `gold_purchase_order_summary`
**Description**: High-level operational summary of all corporate purchase orders.  
**Granularity**: Exactly one row per purchase order.

| Column Name | Data Type | Description |
|---|---|---|
| `po_id` | VARCHAR(32) | Unique PO identifier. |
| `vendor_name` | VARCHAR(255) | Supplier name. |
| `department_name` | VARCHAR(128) | Ordering department. |
| `order_date` | DATE | Date PO was executed. |
| `promised_delivery_date` | DATE | Expected delivery date. |
| `po_status` | VARCHAR(32) | Status (`Fulfilled`, `Partially Fulfilled`, `Cancelled`, `Open`). |
| `total_po_amount` | NUMERIC(15, 2) | Total monetary value of order. |
| `buyer_name` | VARCHAR(128) | Procurement agent responsible for order. |
| `is_fulfilled` | INTEGER | 1 if fulfilled, 0 otherwise. |
| `is_cancelled` | INTEGER | 1 if cancelled, 0 otherwise. |
| `total_line_items` | BIGINT | Number of line items on PO. |
| `total_units_ordered` | BIGINT | Sum of all SKU quantities ordered. |

---

### 7. `gold_category_performance`
**Description**: Procurement category benchmarks, supplier concentration, and spend totals.  
**Granularity**: Exactly one row per category.

| Column Name | Data Type | Description |
|---|---|---|
| `category_id` | VARCHAR(32) | Category identifier (`CAT-001` to `CAT-007`). |
| `category_name` | VARCHAR(128) | Category name (e.g., `Raw Industrial Materials`). |
| `spend_tier` | VARCHAR(64) | Strategic criticality (`Tier 1 - Strategic`, `Tier 2 - Operational`). |
| `active_suppliers_count` | BIGINT | Distinct vendors supplying in this category. |
| `active_skus_count` | BIGINT | Distinct products purchased in this category. |
| `total_orders_placed` | BIGINT | Total purchase orders placed. |
| `total_category_spend` | NUMERIC(15, 2) | Gross spend expended in category ($). |
| `avg_unit_price` | NUMERIC(12, 2) | Mean unit purchase price. |
| `avg_order_quantity` | NUMERIC(10, 2) | Mean line item order quantity. |
