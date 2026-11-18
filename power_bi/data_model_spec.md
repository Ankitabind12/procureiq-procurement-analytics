# Power BI Semantic Data Model Specification
## ProcureIQ Enterprise Star Schema Architecture

---

### 1. Conceptual Model Overview
The ProcureIQ reporting model follows Ralph Kimball dimensional modeling best practices. It features three central Fact tables capturing distinct business events across the procurement lifecycle, surrounded by five shared Conformed Dimensions.

```
                      +-------------------+
                      |   dim_category    |
                      +-------------------+
                                | 1
                                | *
  +------------------+ 1      * +--------------------+ 1      * +------------------+
  |   dim_product    |----------| fact_purchase_orders |----------|  dim_department  |
  +------------------+          +--------------------+          +------------------+
                                        | *
                                        | 1
                                +-------------------+
                                |    dim_vendor     |
                                +-------------------+
                                  | 1             | 1
                                  | *             | *
                    +-------------------+     +-----------------+
                    |  fact_deliveries  |     |  fact_invoices  |
                    +-------------------+     +-----------------+
                                  | *             | *
                                  | 1             | 1
                                +-------------------+
                                |     dim_date      |
                                +-------------------+
```

---

### 2. Table Catalog & Granularity (Grain)

| Table Name | Type | Grain (What 1 row represents) | Primary / Surrogate Key | Row Count |
|---|---|---|---|---|
| **`fact_purchase_orders`** | Fact | One individual line item on a purchase order. | `line_item_id` | 9,118 |
| **`fact_deliveries`** | Fact | One physical shipment arrival & inspection event. | `delivery_id` | 5,000 |
| **`fact_invoices`** | Fact | One vendor billing invoice and 3-way reconciliation record. | `invoice_id` | 5,000 |
| **`dim_vendor`** | Dimension | One unique vendor/supplier profile. | `vendor_id` | 500 |
| **`dim_product`** | Dimension | One unique material SKU or purchased item. | `product_id` | 100 |
| **`dim_department`** | Dimension | One internal business department/cost center. | `department_id` | 8 |
| **`dim_date`** | Dimension | One calendar day (calendar & fiscal hierarchies). | `date_key` (YYYYMMDD) | 1,096 |
| **`dim_category`** | Dimension | One procurement commodity category. | `category_id` | 7 |

---

### 3. Star Schema Relationship Specifications

| From (Fact Table) | Foreign Key | To (Dimension Table) | Primary Key | Cardinality | Cross-Filter Direction | Active Status |
|---|---|---|---|---|---|---|
| `fact_purchase_orders` | `vendor_id` | `dim_vendor` | `vendor_id` | Many to One (*:1) | Single (`dim_vendor` filters `fact`) | **Active** |
| `fact_purchase_orders` | `product_id` | `dim_product` | `product_id` | Many to One (*:1) | Single (`dim_product` filters `fact`) | **Active** |
| `fact_purchase_orders` | `department_id` | `dim_department` | `department_id` | Many to One (*:1) | Single (`dim_department` filters `fact`) | **Active** |
| `fact_purchase_orders` | `order_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single (`dim_date` filters `fact`) | **Active** |
| `fact_purchase_orders` | `promised_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single | Inactive (Use `USERELATIONSHIP`) |
| `fact_deliveries` | `vendor_id` | `dim_vendor` | `vendor_id` | Many to One (*:1) | Single (`dim_vendor` filters `fact`) | **Active** |
| `fact_deliveries` | `actual_delivery_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single (`dim_date` filters `fact`) | **Active** |
| `fact_invoices` | `vendor_id` | `dim_vendor` | `vendor_id` | Many to One (*:1) | Single (`dim_vendor` filters `fact`) | **Active** |
| `fact_invoices` | `invoice_date_key` | `dim_date` | `date_key` | Many to One (*:1) | Single (`dim_date` filters `fact`) | **Active** |
| `dim_vendor` | `primary_category_id` | `dim_category` | `category_id` | Many to One (*:1) | Single (`dim_category` filters `dim_vendor`) | **Active** |
| `dim_product` | `category_id` | `dim_category` | `category_id` | Many to One (*:1) | Single (`dim_category` filters `dim_product`) | **Active** |

---

### 4. Direct Mart Integration (Pre-Aggregated Gold Marts)
For rapid report development or executive dashboard consumption without joining granular fact rows, the following pre-compiled Gold Marts are directly available:
1. `gold_vendor_scorecard` (500 rows - 1 row per vendor)
2. `gold_procurement_spend` (1,792 rows - aggregated monthly spend by dept & category)
3. `gold_delivery_performance` (2,628 rows - carrier & vendor delivery trends)
4. `gold_invoice_analysis` (1,107 rows - AP discrepancy breakdown)
5. `gold_compliance_status` (500 rows - certification audit log)
6. `gold_purchase_order_summary` (5,000 rows - PO header level operational tracker)
7. `gold_category_performance` (7 rows - category high-level benchmarks)

---

### 5. Best Practices & Optimization Guidelines
- **Storage Mode**: Import mode recommended for sub-second report interactivity.
- **Date Keys**: Integer format (`YYYYMMDD`, e.g., `20241015`) avoids string parsing overhead and optimizes VertiPaq column compression.
- **Cross-Filter**: Kept strictly to Single direction to prevent ambiguous filter paths and circular dependencies.
