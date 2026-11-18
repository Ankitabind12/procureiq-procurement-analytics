# ProcureIQ: Data Warehouse Architecture Document
## Medallion Lakehouse & Warehouse Standard (Bronze &bull; Silver &bull; Gold)

---

### 1. Architectural Philosophy
ProcureIQ implements the industry-standard **Medallion Architecture**, separating the data lifecycle into three distinct maturity tiers to guarantee auditability, referential integrity, and sub-second analytical querying.

```
+---------------------------------------------------------------------------------------+
| BRONZE LAYER: Raw Ingestion                                                          |
| - Pure source fidelity; zero lossy transformations.                                   |
| - Schema-on-read flexibility with appended audit tracking metadata.                  |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| SILVER LAYER: Cleaned, Conformed, & Validated                                         |
| - Referential integrity enforcement across POs, Deliveries, and Invoices.             |
| - Standardized ISO dates (YYYY-MM-DD), cleaned string casings, and deduplication.     |
| - Operational derivations (delay days, discrepancy amounts, compliance risk tiers).   |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| GOLD LAYER: Analytical Marts & Star Schema                                            |
| - Ralph Kimball Star Schema (3 Fact Tables + 5 Conformed Dimensions).                 |
| - 7 Dedicated Business Marts for self-service Power BI and executive BI reporting.    |
| - 4-Pillar Transparent Supplier Scoring Algorithm.                                    |
+---------------------------------------------------------------------------------------+
```

---

### 2. Layer Deep Dive

#### 2.1 Bronze Layer (Raw & Auditable)
- **Design Rule**: Records are loaded as close to raw source format as possible.
- **Audit Columns Appended**:
  - `_ingested_at TIMESTAMP`: Exact UTC timestamp when the record entered the warehouse.
  - `_source_file VARCHAR(255)`: Original filename for data lineage.
  - `_batch_id VARCHAR(64)`: Unique execution run ID for incremental tracking and rollbacks.
- **Tables**: `bronze_departments`, `bronze_categories`, `bronze_products`, `bronze_date_dimension`, `bronze_vendors`, `bronze_vendor_compliance`, `bronze_purchase_orders`, `bronze_purchase_order_items`, `bronze_deliveries`, `bronze_invoices`.

#### 2.2 Silver Layer (Cleansed & Conformed)
- **Data Cleansing Rules**:
  - Whitespace trimmed (`TRIM()`), email addresses downcased (`LOWER()`).
  - Dates standardized to SQL `DATE` format (`YYYY-MM-DD`).
  - Numerical currency fields standardized to `NUMERIC(15, 2)`.
  - Negative or impossible quantities filtered out.
- **Integrity Validation**:
  - Deliveries without a corresponding active PO are flagged.
  - Invoices are checked for 3-way matching against PO headers and delivery quantities.
- **Business Derivations**:
  - `delay_days`: Difference between actual delivery date and promised delivery date.
  - `delay_bucket`: Categorized into `On-Time`, `1-7 Days Delay`, `8-14 Days Delay`, `15+ Days Severe Delay`.
  - `discrepancy_amount`: Invoice billed amount minus PO contracted amount.
  - `compliance_risk_tier`: Tagged as `HIGH RISK - EXPIRED`, `MEDIUM RISK - EXPIRING SOON`, or `LOW RISK - VALID`.

#### 2.3 Gold Layer (Business Marts & Semantic Facts/Dims)
- **Star Schema Dimensions**: `dim_vendor`, `dim_product`, `dim_department`, `dim_date`, `dim_category`.
- **Star Schema Facts**: `fact_purchase_orders` (Grain: line item), `fact_deliveries` (Grain: shipment), `fact_invoices` (Grain: invoice).
- **The 7 Certified Business Marts**:
  1. `gold_vendor_scorecard`: 360-degree supplier scorecard with 4-pillar scores and tier badges.
  2. `gold_procurement_spend`: Monthly temporal spend distributions across cost centers.
  3. `gold_delivery_performance`: Carrier and supplier logistics reliability.
  4. `gold_invoice_analysis`: Accounts Payable leakage and variance breakdown.
  5. `gold_compliance_status`: Real-time regulatory audit status and expiry guardrails.
  6. `gold_purchase_order_summary`: PO lifecycle health tracker.
  7. `gold_category_performance`: Category-level market pricing and supplier concentration.

---

### 3. Dual Storage Engine Strategy
ProcureIQ is engineered for zero-friction portability:
1. **Local Embedded Warehouse (DuckDB)**:
   - Zero-dependency OLAP database engine.
   - Executes full ANSI SQL, window functions, and Star Schema joins with columnar speed.
   - Ideal for instant local review, unit testing, and GitHub Actions CI pipelines.
2. **Enterprise Warehouse (PostgreSQL)**:
   - Full ACID-compliant production deployment.
   - Enabled seamlessly by setting `DB_ENGINE=postgresql` in `.env`.
   - Includes dedicated SQL DDL scripts compatible with PostgreSQL 13+.
