# ProcureIQ: Execution & Operations Guide

This guide explains how to execute, operate, and validate the ProcureIQ pipeline across all operational modes.

---

### 1. One-Click Automated Master Execution
To execute the complete end-to-end Medallion data engineering lifecycle in a single command:

```bash
python run_pipeline.py
```

This single command automatically:
1. Verifies/synthesizes 500+ vendors, 5,000+ POs, 9,000+ line items, 5,000 deliveries, 5,000 invoices.
2. Ingests all tables into the **Bronze Layer** with operational audit metadata.
3. Cleans, standardizes, and validates referential integrity in the **Silver Layer**.
4. Builds the Ralph Kimball **Star Schema** and compiles all seven **Gold Analytical Marts**.
5. Computes the 10 core executive procurement KPIs and 4-pillar vendor performance ratings.
6. Executes statistical price anomaly detection (Z-scores) and chronic delay risk scans.
7. Exports 15 certified business tables to `data/gold_exports/*.csv` for Power BI consumption.

---

### 2. Step-by-Step Modular Execution
Each pipeline component can also be invoked independently for granular debugging:

#### Step 2.1: Generate Realistic Procurement Data
```bash
python -m src.generator.data_generator
```
*Output*: Generates 10 raw CSV files into `data/raw/`.

#### Step 2.2: Bronze Layer Ingestion
```bash
python -m src.ingestion.bronze_loader
```
*Output*: Loads `bronze_*` tables into the warehouse with UTC audit timestamps and batch IDs.

#### Step 2.3: Silver Cleansing & Transformation
```bash
python -m src.transformation.silver_transformer
```
*Output*: Builds `silver_*` tables with standardized ISO dates, delay metrics, and discrepancy flags.

#### Step 2.4: Gold Layer & Star Schema Modeling
```bash
python -m src.gold.gold_builder
```
*Output*: Compiles the 7 Gold Marts and 8 Star Schema views (`fact_*`, `dim_*`).

#### Step 2.5: Compute Executive KPIs
```bash
python -m src.gold.kpi_engine
```
*Output*: Computes 10 core KPIs and writes `docs/kpi_summary_results.json`.

#### Step 2.6: Run Statistical Anomaly Detection
```bash
python -m src.analytics.anomaly_detector
```
*Output*: Flags price anomalies and chronic delay vendors; writes `docs/anomaly_detection_report.json`.

#### Step 2.7: Export Power BI Datasets
```bash
python -m power_bi.export_powerbi_data
```
*Output*: Exports 15 CSV datasets to `data/gold_exports/`.

---

### 3. Launching the Interactive Executive Dashboard
ProcureIQ includes a rich, self-contained executive dashboard preview:

- **Option A (Direct File)**: Double-click or open `power_bi/interactive_dashboard_preview.html` in any modern web browser (Chrome, Edge, Firefox, Safari).
- **Option B (Local Web Server)**:
  ```bash
  python -m http.server 8080 --directory power_bi
  ```
  Then visit `http://localhost:8080/interactive_dashboard_preview.html`.

---

### 4. Running dbt (Data Build Tool) Models
If using dbt for warehouse modeling:
```bash
cd dbt_procureiq
dbt deps
dbt run --profiles-dir .
dbt test --profiles-dir .
```

---

### 5. Running the Automated Test Suite
Execute the comprehensive Pytest verification suite:
```bash
pytest -v
```
To run specific test modules:
```bash
pytest tests/test_data_integrity.py -v
pytest tests/test_kpi_calculations.py -v
pytest tests/test_pipeline.py -v
```
