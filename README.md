# ProcureIQ: Intelligent Procurement & Vendor Performance Analytics Platform

[![Python 3.10](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/Engine-DuckDB%20%7C%20PostgreSQL-yellow.svg)](https://duckdb.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20(Bronze%20%E2%86%92%20Silver%20%E2%86%92%20Gold)-brightgreen.svg)](docs/data_warehouse_architecture.md)
[![Data Modeling](https://img.shields.io/badge/Modeling-Kimball%20Star%20Schema-purple.svg)](docs/star_schema_diagram.md)
[![Power BI](https://img.shields.io/badge/Power%20BI-Semantic%20Model%20%2B%20DAX-F2C811.svg)](power_bi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests: Pytest](https://img.shields.io/badge/Tests-11%20Passed%20(100%25)-success.svg)](tests/)

> An end-to-end, enterprise-grade Procurement Analytics and Vendor Performance Data Warehouse built using Python, PostgreSQL/DuckDB, Medallion Lakehouse Architecture, dbt-compatible models, and Power BI.

---

## Table of Contents
- [Executive Overview](#executive-overview)
- [The Real-World Business Problem](#the-real-world-business-problem)
- [The Solution: ProcureIQ Platform](#the-solution-procureiq-platform)
- [System & Data Warehouse Architecture](#system--data-warehouse-architecture)
- [Medallion Architecture (Bronze &bull; Silver &bull; Gold)](#medallion-architecture)
- [Dimensional Star Schema Design](#dimensional-star-schema-design)
- [Key Procurement KPIs & Empirical Results](#key-procurement-kpis--empirical-results)
- [Transparent 4-Pillar Vendor Scoring Engine](#transparent-4-pillar-vendor-scoring-engine)
- [Advanced Anomaly Detection & AI Guardrails](#advanced-anomaly-detection--ai-guardrails)
- [Power BI Reporting Suite](#power-bi-reporting-suite)
- [Project Directory Structure](#project-directory-structure)
- [Installation & Quick Start](#installation--quick-start)
- [Testing & Validation](#testing--validation)
- [Business Impact & Strategic Recommendations](#business-impact--strategic-recommendations)
- [Technical Limitations & Future Roadmap](#technical-limitations--future-roadmap)
- [Author & Portfolio Contact](#author--portfolio-contact)

---

## Executive Overview
In mid-to-large enterprises, procurement operations manage hundreds of external suppliers and tens of thousands of purchase orders annually. However, transactional data typically fragments across ERP databases, receiving dock inspections, Accounts Payable ledgers, and vendor compliance repositories.

**ProcureIQ** centralizes multi-source procurement data into an auditable Medallion Data Warehouse, executes automated data quality gates, and generates certified Gold analytical marts to deliver actionable sourcing intelligence, eliminate financial overbilling leakage, and objectively rank suppliers.

---

## The Real-World Business Problem
Procurement and finance teams routinely struggle with critical operational blind spots:
1. **Unmonitored Vendor Delivery Delays**: Critical raw materials arrive late without warning, causing production stoppages.
2. **Price Dispersion & Uncontrolled Spend**: Sourcing teams pay vastly different unit prices for identical material SKUs across suppliers.
3. **Accounts Payable Invoice Leakage**: Invoices often bypass contracted PO rates or bill for undelivered units (failing 3-way matching).
4. **Subjective Supplier Evaluations**: Vendor contract renewals are negotiated on gut feeling rather than auditable, multi-pillar empirical performance metrics.
5. **Regulatory & Documentation Exposure**: Suppliers operate with lapsed ISO certifications or expired liability insurance, creating legal vulnerability.

---

## The Solution: ProcureIQ Platform
ProcureIQ solves these challenges through an automated end-to-end data pipeline:
- **Scalable Ingestion**: Captures transactions across 500+ vendors, 5,000+ purchase orders, 9,118 line items, 5,000 deliveries, and 5,000 invoices.
- **Medallion Data Lakehouse Architecture**: Enforces data quality gates from Bronze (raw audit), Silver (conformed & validated), to Gold (analytical marts).
- **Kimball Star Schema**: Structured fact and dimension tables optimized for high-performance analytical queries.
- **Automated KPI Engine**: Calculates 10 core procurement KPIs, including Accounts Payable dollar leakage and OTIF (On-Time In-Full) rates.
- **Machine Learning & Statistical Anomaly Detection**: Z-Score price outlier flags and chronic delivery delay risk alerts.
- **Power BI Semantic Modeling**: Certified DAX measures and interactive executive dashboards.

---

## System & Data Warehouse Architecture

```mermaid
flowchart TD
    subgraph Sources["1. Operational Source Data"]
        S1["ERP Purchase Orders\n(5,000+ POs, 9,118 Line Items)"]
        S2["Receiving Dock WMS\n(5,000+ Deliveries & QC Inspections)"]
        S3["Accounts Payable\n(5,000+ Billing Invoices)"]
        S4["Vendor & Compliance Portal\n(500+ Suppliers, 500+ Certs)"]
    end

    subgraph Pipeline["2. Python ELT Orchestration (run_pipeline.py)"]
        P1["Bronze Loader\n(Audit Metadata Stamping)"]
        P2["Silver Transformer\n(Deduplication & Conformance)"]
        P3["Gold Builder\n(Star Schema & Aggregations)"]
        P4["KPI & Anomaly Engine\n(Statistical Z-Score & Risk)"]
    end

    subgraph Warehouse["3. Medallion Warehouse (DuckDB / PostgreSQL)"]
        B["BRONZE LAYER\n(Raw Tables + _ingested_at, _source_file, _batch_id)"]
        S["SILVER LAYER\n(Cleaned, Deduplicated, ISO Dates, Delay Tags, Discrepancies)"]
        G["GOLD LAYER\n(7 Certified Marts: Scorecard, Spend, Delivery, AP, Compliance)"]
        B --> S --> G
    end

    subgraph Presentation["4. BI & Sourcing Analytics"]
        BI1["Power BI Semantic Model\n(Certified DAX Measures)"]
        BI2["Interactive HTML Dashboard\n(5-Page Executive Suite)"]
        BI3["SQL Analytical Queries\n(Senior Business Analyst Pack)"]
    end

    Sources --> Pipeline
    Pipeline --> Warehouse
    Warehouse --> Presentation
```

---

## Medallion Architecture

### 1. Bronze Layer (Raw & Auditable)
- Preserves raw source records with exact fidelity.
- Adds operational lineage columns: `_ingested_at`, `_source_file`, and `_batch_id`.
- Tables: `bronze_vendors`, `bronze_purchase_orders`, `bronze_purchase_order_items`, `bronze_deliveries`, `bronze_invoices`, `bronze_vendor_compliance`, `bronze_departments`, `bronze_categories`, `bronze_products`, `bronze_date_dimension`.

### 2. Silver Layer (Cleaned, Conformed, & Validated)
- Enforces referential integrity between POs, Line Items, Deliveries, and Invoices.
- Deduplicates records and cleans string formats (`TRIM()`, `LOWER()`).
- Normalizes all dates to ISO `DATE` (`YYYY-MM-DD`).
- Derives operational indicators: `delay_days`, `delay_bucket`, `discrepancy_amount`, `is_ontime`, `compliance_risk_tier`.

### 3. Gold Layer (Business Marts & Star Schema)
- Consists of Ralph Kimball dimensional models and seven pre-compiled business marts:
  1. `gold_vendor_scorecard`: 360-degree supplier scorecard with 4-pillar scores and tier badges.
  2. `gold_procurement_spend`: Monthly temporal spend distributions across cost centers.
  3. `gold_delivery_performance`: Carrier and supplier logistics reliability.
  4. `gold_invoice_analysis`: Accounts Payable leakage and 3-way match variance breakdown.
  5. `gold_compliance_status`: Real-time regulatory audit status and expiry guardrails.
  6. `gold_purchase_order_summary`: PO lifecycle health tracker.
  7. `gold_category_performance`: Category-level market pricing and supplier concentration.

---

## Dimensional Star Schema Design

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

- **`fact_purchase_orders`** (Grain: One row per PO Line Item &bull; 9,118 rows)
- **`fact_deliveries`** (Grain: One row per receiving dock shipment &bull; 5,000 rows)
- **`fact_invoices`** (Grain: One row per vendor billing invoice &bull; 5,000 rows)
- **Conformed Dimensions**: `dim_vendor` (500), `dim_product` (100), `dim_department` (8), `dim_date` (1,096), `dim_category` (7).

---

## Key Procurement KPIs & Empirical Results
Calculated directly from the actual warehouse data without fabricated assumptions:

| KPI # | Metric Name | Pipeline Value | Benchmark / SLA Target | Status |
|---|---|---|---|---|
| **KPI-01** | **Total Procurement Spend** | **$556,519,550.55** | Within Corporate Budget | Validated |
| **KPI-02** | **On-Time Delivery Rate** | **87.14%** | &ge; 88.0% | Near Target (-0.86%) |
| **KPI-03** | **Average Delivery Delay** | **0.99 Days** | &le; 1.5 Days | Target Achieved |
| **KPI-04** | **PO Fulfilment Rate** | **74.68%** | &ge; 75.0% | Target Achieved |
| **KPI-05** | **Invoice Discrepancy Rate** | **17.02%** (851 Invoices) | &le; 10.0% | High Risk Alert |
| **KPI-06** | **Vendor Compliance Rate** | **79.60%** (71 Expired) | &ge; 90.0% | Immediate Audit Required |
| **KPI-07** | **Average Purchase Order Value** | **$111,303.91** | Baseline Metric | Tracked |
| **KPI-08** | **Top Department Spend** | **Packaging & Assembly ($80.43M / 14.45%)** | Monitored | Reconciled |
| **KPI-09** | **Average Vendor Performance Score** | **92.40 / 100** | &ge; 80.0 / 100 | Target Achieved |
| **KPI-10** | **PO Cancellation Rate** | **8.50%** | &le; 8.0% | Minor Leakage (+0.5%) |
| **ALERT** | **Total AP Invoice Leakage** | **$14,074,490.48** | $0.00 | Blocked by 3-Way Match |

---

## Transparent 4-Pillar Vendor Scoring Engine
Suppliers are graded on an objective 100-point composite algorithm:

$$\text{Composite Score} = 0.35(\text{Delivery}) + 0.25(\text{Price}) + 0.25(\text{Quality}) + 0.15(\text{Compliance})$$

1. **Delivery Reliability (35% Weight)**: Evaluates contractual on-time shipment rate.
2. **Price Competitiveness (25% Weight)**: Normalized variance relative to category SKU standard costs.
3. **Product Quality (25% Weight)**: Receiving dock inspection pass rate and defect-free percentage.
4. **Documentation Compliance (15% Weight)**: ISO certifications, environmental compliance, and audit ratings.

### Performance Tier Breakdown:
- **Tier 1 - Strategic Partner** (Score &ge; 88): 392 Vendors (Eligible for consolidated preferred volume).
- **Tier 2 - Preferred Supplier** (Score 75 - 87.9): 106 Vendors (Reliable baseline fulfillment).
- **Tier 3 - Operational Supplier** (Score 60 - 74.9): 2 Vendors (Monitored for delivery/pricing variances).
- **Tier 4 - High Risk / PIP Required** (Score < 60): Vendors subject to immediate PO holds.

---

## Advanced Anomaly Detection & AI Guardrails
Implemented in `src/analytics/anomaly_detector.py`:
- **Statistical Price Outlier Detection**: Computes category-level Z-Scores on unit price paid vs standard SKU costs. Flagged **291 pricing anomalies** representing **$38.2M in excess cost exposure**.
- **Chronic Delay Vendor Identification**: Scans for suppliers with persistent delivery delays (>40% late rate across 5+ shipments). Flagged **26 chronic delay vendors**, including *Global Fabricators* (41.67% on-time, 4.25 days avg delay across $4.37M in spend).
- **Compliance Expiry Guardrails**: Automated scanning identified **71 expired certificates** and **30 certificates expiring in &le; 45 days**, triggering automatic stop-shipment recommendations.

---

## Power BI Reporting Suite
Located in `power_bi/`:
- **Page 1: Procurement Overview**: Macro spend volume ($556.52M), department budgets, and category splits.
- **Page 2: Vendor Performance**: 4-pillar quadrant scatter plot, scorecards, and tier distribution.
- **Page 3: Delivery Analytics**: On-time vs delay trends, carrier benchmarks (FedEx, DHL, Maersk), and delay buckets.
- **Page 4: Invoice & Spending Reconciliation**: AP discrepancy root-cause waterfall and $14.07M leakage breakdown.
- **Page 5: Compliance Monitoring**: Real-time ISO/insurance audit matrix and high-risk supplier holds.
- **Interactive Browser Preview**: Open `power_bi/interactive_dashboard_preview.html` to test the live dashboard in your web browser!

---

## Project Directory Structure

```
procureiq-procurement-analytics/
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── requirements.txt
├── run_pipeline.py                     # Master 1-Click Pipeline Orchestrator
│
├── data/
│   ├── raw/                            # Generated source CSV datasets (10 files)
│   ├── processed/                      # Cleaned staging records
│   └── gold_exports/                   # Certified Power BI CSV/parquet exports (15 tables)
│
├── docs/                               # Comprehensive Enterprise Documentation
│   ├── brd.md                          # Business Requirements Document
│   ├── system_architecture.md          # System Architecture & Component Lineage
│   ├── data_warehouse_architecture.md  # Medallion Lakehouse Architecture Standard
│   ├── er_diagram.md                   # Relational Entity-Relationship Diagram
│   ├── star_schema_diagram.md          # Ralph Kimball Dimensional Star Schema
│   ├── etl_pipeline_docs.md            # ELT Execution, Idempotency & Audit Logs
│   ├── kpi_dictionary.md               # 10 Core KPIs & 4-Pillar Score Formula
│   ├── gold_data_dictionary.md         # Column-by-Column Data Dictionary for Marts
│   ├── business_recommendations.md     # Strategic Sourcing Insights & Action Plans
│   ├── installation_guide.md           # Local & Enterprise Setup Guide
│   ├── execution_guide.md              # CLI Operation & dbt Execution Guide
│   └── testing_documentation.md        # Quality Assurance & Test Case Matrix
│
├── src/                                # Core Python Source Code
│   ├── config.py                       # Configuration & Environment Handler
│   ├── utils/logger.py                 # Structured Logger (Console + Logfile)
│   ├── generator/data_generator.py     # Realistic Synthetic Procurement Synthesizer
│   ├── ingestion/bronze_loader.py      # Bronze Ingestion with Operational Metadata
│   ├── transformation/silver_transformer.py # Silver Cleansing & Referential Integrity
│   ├── gold/gold_builder.py            # Gold Marts Compilation & Star Schema Views
│   ├── gold/kpi_engine.py              # Automated 10-KPI Calculation Engine
│   └── analytics/anomaly_detector.py   # Statistical Z-Score Outlier & Delay Risk Engine
│
├── sql/                                # Pure ANSI SQL DDL & Transformation Scripts
│   ├── 01_bronze_ddl.sql               # Bronze Ingestion DDL with Audit Columns
│   ├── 02_silver_transformations.sql   # Silver Cleansing, Deduplication & Validation
│   ├── 03_gold_marts.sql               # 7 Certified Gold Analytical Marts
│   ├── 04_star_schema_views.sql        # Ralph Kimball Fact and Dimension Views
│   └── 05_analytical_business_queries.sql # Senior Business Analyst SQL Query Pack
│
├── dbt_procureiq/                      # dbt (Data Build Tool) Modeling Project
│   ├── dbt_project.yml
│   ├── profiles.yml.example
│   ├── models/staging/                 # Staging Views with Schema Validation Tests
│   └── models/marts/                   # Gold Analytical Mart Models
│
├── power_bi/                           # Power BI Business Intelligence Assets
│   ├── dax_measures.md                 # Certified Enterprise DAX Library (30+ Measures)
│   ├── data_model_spec.md              # Star Schema Relationships & Cardinality Spec
│   ├── dashboard_design_guide.md       # 5-Page Visual Wireframes & Color Palette
│   ├── export_powerbi_data.py          # Automated Exporter for Power BI Datasets
│   └── interactive_dashboard_preview.html # Live Interactive Executive Web Dashboard
│
└── tests/                              # Automated Pytest Suite
    ├── test_data_integrity.py          # Referential Integrity & Foreign Key Tests
    ├── test_kpi_calculations.py        # KPI Boundary & Status Distribution Tests
    └── test_pipeline.py                # Pipeline Idempotency & Export Tests
```

---

## Installation & Quick Start

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/Ankitabind12/procureiq-procurement-analytics.git
cd procureiq-procurement-analytics
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Complete Pipeline (1-Click)
```bash
python run_pipeline.py
```

### 4. Open the Interactive Executive Dashboard
Open `power_bi/interactive_dashboard_preview.html` in any web browser to explore interactive charts, scorecards, and leakage breakdowns!

---

## Testing & Validation
Run the automated Pytest test suite:
```bash
pytest -v
```
All **11 unit and data integrity tests** pass with 100% success rate:
- Referential integrity between POs, Deliveries, Invoices, and Vendors.
- Mathematical boundaries on all KPIs (rates bounded between 0% and 100%).
- Full pipeline idempotency (repeated runs produce zero duplicate rows).

---

## Business Impact & Strategic Recommendations
1. **Accounts Payable Leakage Containment**: Enforcing a strict &plusmn;1% automated 3-way match tolerance locks down **$14.07M in invoice overbilling variance**.
2. **Supplier Consolidation Savings**: Sourcing in Packaging ($96.17M) and Professional Services ($89.29M) is fragmented across >75 vendors per category. Consolidating to 15 preferred Tier-1 partners can drive **$15M–$20M in negotiated volume savings (6–8%)**.
3. **Supply Chain Continuity**: Freeze purchase order issuance to *Global Fabricators* ($4.37M spend, 41.67% on-time delivery) until an auditable Performance Improvement Plan is passed.
4. **Compliance Liability Mitigation**: Enforce an automated ERP purchase order freeze on all **71 vendors operating with expired insurance or ISO certifications**.

---

## Technical Limitations & Future Roadmap
- **Batch vs Real-Time Streaming**: ProcureIQ currently runs on high-speed scheduled micro-batches. Future iterations will integrate Apache Kafka for streaming dock barcode scans.
- **Direct ERP Write-Back**: Present implementation reads from operational extracts. Future roadmap includes bi-directional SAP/Oracle REST API connectors to post debit memos automatically.

---

## Author & Portfolio Contact
- **Developer**: Ankita Bind
- **GitHub**: [@Ankitabind12](https://github.com/Ankitabind12)
- **Repository**: [https://github.com/Ankitabind12/procureiq-procurement-analytics](https://github.com/Ankitabind12/procureiq-procurement-analytics)
- **Target Positions**: Junior Data Engineer &bull; Data Intelligence Analyst &bull; Junior Business Analyst
