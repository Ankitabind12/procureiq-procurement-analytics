# Business Requirements Document (BRD)
## Project: ProcureIQ – Intelligent Procurement & Vendor Performance Analytics Platform

---

### 1. Document Control
- **Project Name**: ProcureIQ (Enterprise Procurement & Vendor Intelligence Platform)
- **Document Version**: 1.0.0
- **Document Status**: Approved / Baseline
- **Target Roles**: Junior Data Engineer, Data Intelligence Analyst, Junior Business Analyst
- **Architecture Standard**: Medallion Data Lakehouse / Warehouse Architecture (Bronze -> Silver -> Gold)

---

### 2. Executive Summary & Business Problem Statement
Modern mid-to-large enterprises procure millions of dollars in direct raw materials, capital equipment, MRO (maintenance, repair, and operations) items, and professional services across hundreds of external suppliers. 

However, procurement operations routinely suffer from fragmented transactional data, leading to severe operational and financial vulnerabilities:
1. **Unmonitored Vendor Delivery Delays**: Production lines stall when Tier-1 vendors deliver late without prior warning.
2. **Uncontrolled Spend & Price Dispersion**: Identical material SKUs are purchased from different vendors at widely fluctuating unit prices.
3. **Purchase Order (PO) Fulfillment Gaps**: High cancellation and partial delivery rates inflate inventory holding and administrative overhead.
4. **Invoice Discrepancies & Overbilling**: Invoices frequently deviate from contracted PO terms in quantity and unit cost (failing 3-way matching).
5. **Regulatory & Documentation Compliance Vulnerabilities**: Vendors operate with expired ISO certifications, lapsed insurance, or invalid tax compliance, creating legal liability.
6. **Subjective Supplier Evaluation**: Vendor renewals are negotiated on gut feelings rather than auditable, multi-pillar empirical performance metrics.

**ProcureIQ** addresses these challenges by consolidating disparate procurement data into an auditable PostgreSQL/DuckDB Medallion Data Warehouse, transforming raw transactions into certified Gold Data Marts, and serving executive BI dashboards with automated anomaly detection.

---

### 3. Business Objectives & Success Metrics
| Objective ID | Business Objective | Target KPI / Success Metric |
|---|---|---|
| **OBJ-01** | Centralize multi-source procurement data | 100% of POs, Deliveries, Invoices, and Compliance records unified in Bronze/Silver layers. |
| **OBJ-02** | Eliminate invoice overpayment leakage | Detect and flag 100% of quantity/price invoice mismatches exceeding 1% tolerance. |
| **OBJ-03** | Increase On-Time In-Full (OTIF) deliveries | Improve vendor delivery tracking to achieve >= 88% overall on-time delivery rate. |
| **OBJ-04** | Objective Vendor Performance Scorecard | Automated transparent scoring (Reliability 35%, Price 25%, Quality 25%, Compliance 15%). |
| **OBJ-05** | Mitigate supplier compliance risk | Real-time flagging of expired or near-expiry regulatory certificates. |
| **OBJ-06** | Enable self-service enterprise analytics | Deliver Star Schema models and Power BI measures for cross-functional drill-down. |

---

### 4. Stakeholder Matrix
| Stakeholder Role | Responsibilities | Key Information Needs |
|---|---|---|
| **Chief Procurement Officer (CPO)** | Strategic sourcing, budget governance, vendor risk management. | Macro spend trends, high-risk suppliers, executive scorecard rankings. |
| **Category Managers** | Negotiating contracts, evaluating SKU price competitiveness. | Price variance across suppliers, category spend distribution, contract compliance. |
| **Procurement Operations Team** | Managing PO lifecycles, monitoring shipments. | PO fulfillment rates, lead time delays, delivery status alerts. |
| **Accounts Payable (AP)** | Reconciling and settling vendor invoices. | Invoice discrepancies (PO amount vs Invoice amount, line item quantity variations). |
| **Quality & Compliance Officers** | Auditing supplier certifications and ESG/safety standards. | Document expiry dates, audit pass rates, defective item percentages. |
| **Data & BI Engineering Team** | Building and maintaining ELT pipelines, schemas, and dashboards. | Data warehouse SLA, data quality tests, schema lineage, refresh performance. |

---

### 5. Functional Requirements
- **FR-01: Multi-Entity Ingestion (Bronze Layer)**:
  Ingest raw transactional CSV files (Vendors, POs, PO Line Items, Deliveries, Invoices, Compliance, Products, Departments) into append-only tables with ingestion timestamps and source lineage tracking.
- **FR-02: Data Cleansing & Integrity Enforcement (Silver Layer)**:
  - Deduplicate records and sanitize text fields (vendor name standardization, case normalization).
  - Handle null values, invalid foreign keys, and date format standardizations (`YYYY-MM-DD`).
  - Validate referential integrity between POs, Line Items, Deliveries, and Invoices.
  - Compute derived status flags (e.g., `is_delayed`, `delay_days`, `is_invoice_mismatch`).
- **FR-03: Dimensional Modeling & Gold Marts (Gold Layer)**:
  Build Star Schema dimensional models (Fact tables: `fact_purchase_orders`, `fact_deliveries`, `fact_invoices`; Dimension tables: `dim_vendor`, `dim_product`, `dim_department`, `dim_date`, `dim_category`).
  Generate seven dedicated analytical marts:
  1. `gold_vendor_scorecard`
  2. `gold_procurement_spend`
  3. `gold_delivery_performance`
  4. `gold_invoice_analysis`
  5. `gold_compliance_status`
  6. `gold_purchase_order_summary`
  7. `gold_category_performance`
- **FR-04: Automated KPI & Performance Calculation Engine**:
  Calculate 10 core procurement KPIs, including the transparent 4-pillar Vendor Performance Score.
- **FR-05: Advanced Anomaly Detection**:
  Identify price outliers per SKU category, predict delivery delay risks, and trigger compliance renewal alerts using statistical thresholds (Z-score / IQR) and rule engines.
- **FR-06: Power BI Semantic Modeling**:
  Provide pre-calculated DAX measures, star-schema data relationships, and automated CSV/parquet exports ready for interactive visual consumption.

---

### 6. Non-Functional Requirements
- **NFR-01: Idempotency & Repeatability**: Running the pipeline multiple times on the same data must produce deterministic results without creating duplicate records or state corruption.
- **NFR-02: Portability & Zero-Friction Setup**: Support both enterprise PostgreSQL connections and embedded DuckDB/SQLite execution for local development without external server dependencies.
- **NFR-03: Security & Privacy**: Zero credentials, database passwords, or personal identifiable secrets committed to source control; configuration mediated strictly through `.env`.
- **NFR-04: Modularity**: Loosely coupled Python modules for data generation, ingestion, transformation, gold mart compilation, analytics, and testing.
- **NFR-05: Auditability**: Detailed logging with execution timestamps, record counts, and failure tracking.

---

### 7. Key Business Questions Solved
1. Which vendors consistently miss agreed delivery lead times, and what is the financial impact of their delays?
2. Which suppliers offer the best unit price for identical materials without compromising on-time delivery or quality?
3. Where are invoice overcharges occurring, and what is the total discrepancy dollar amount?
4. What proportion of vendors are operating with expired insurance or safety certifications?
5. How does procurement spending distribute across business departments and commodity categories?
6. Which vendors qualify as Tier-1 Strategic Partners, and which should be placed on a Performance Improvement Plan (PIP) or phased out?

---

### 8. Project Scope & Assumptions
- **In Scope**:
  - Synthetic data generation modeled after realistic industrial supply chains (500+ vendors, 5,000+ POs, 8,000+ line items, 5,000+ deliveries, 5,000+ invoices).
  - Medallion architecture execution (Bronze, Silver, Gold).
  - Star schema dimensional design with documented grain.
  - Rule-based and statistical anomaly detection.
  - Comprehensive Power BI measures, data model specifications, and SQL analytical views.
  - Pytest verification suite and automated execution runner.
- **Out of Scope**:
  - Real-time streaming ingestion (Kafka/Flink) — batch micro-pipelines are standard for procurement reconciliation.
  - Direct ERP write-back (SAP/Oracle API write-backs) — read-only warehouse integration.
