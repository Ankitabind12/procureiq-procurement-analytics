# ProcureIQ: ETL / ELT Pipeline Documentation

---

### 1. Pipeline Overview
The ProcureIQ data pipeline is a robust, modular, and idempotent ELT workflow designed for modern enterprise procurement analytics. It orchestrates the ingestion of raw multi-source transactional data, standardizes and validates records in the Silver layer, and compiles executive Gold business marts and Star Schema views.

```
Raw CSV Extracts -> Bronze Loader -> Silver Transformer -> Gold Marts -> KPI & Anomaly Engine -> Power BI Exporter
```

---

### 2. Execution Flow & Module Map

| Stage | Module | Input | Output Table(s) | Description |
|---|---|---|---|---|
| **0. Generator** | `src/generator/data_generator.py` | Configuration | `data/raw/*.csv` | Synthesizes 500+ vendors, 5,000+ POs, 9,000+ items, 5,000+ deliveries/invoices with realistic business anomalies. |
| **1. Bronze Ingestion** | `src/ingestion/bronze_loader.py` | `data/raw/*.csv` | `bronze_*` | Appends `_ingested_at`, `_source_file`, `_batch_id` metadata. Loads append-only raw tables. |
| **2. Silver Transformation** | `src/transformation/silver_transformer.py` | `bronze_*` | `silver_*` | Casts ISO dates, standardizes text cases, validates foreign keys, computes operational indicators (`delay_days`, `discrepancy_amount`). |
| **3. Gold Compilation** | `src/gold/gold_builder.py` | `silver_*` | `gold_*` & Facts/Dims | Pre-aggregates the 7 Gold Marts and establishes Ralph Kimball Star Schema fact and dimension tables. |
| **4. KPI Engine** | `src/gold/kpi_engine.py` | `gold_*`, `silver_*` | `docs/kpi_summary_results.json` | Computes the 10 core procurement KPIs and 4-pillar vendor scores. |
| **5. Anomaly Detection** | `src/analytics/anomaly_detector.py` | `silver_*` | `docs/anomaly_detection_report.json` | Executes statistical price outlier detection (Z-Score), chronic delay identification, and compliance expiry scanning. |
| **6. BI Export** | `power_bi/export_powerbi_data.py` | `gold_*`, Facts/Dims | `data/gold_exports/*.csv` | Exports certified datasets formatted for instant 1-click Power BI import. |

---

### 3. Key Data Engineering Principles Implemented

#### 3.1 Idempotency & Repeatability
- The pipeline can be executed an arbitrary number of times on the same input data without producing duplicate records or state corruption.
- Table transformations in the Silver and Gold layers utilize deterministic replace/merge strategies (`DROP TABLE IF EXISTS ...; CREATE TABLE ... AS SELECT ...`).

#### 3.2 Auditability & Lineage Tracking
- Every record in the Bronze layer is tagged with:
  - `_ingested_at`: UTC timestamp of ingestion.
  - `_source_file`: Original file provenance.
  - `_batch_id`: Run identifier formatted as `BATCH-YYYYMMDD-<uuid8>`.

#### 3.3 Data Quality & Referential Integrity Checks
- Purchase orders with negative order quantities or null vendor IDs are rejected during Silver processing.
- Deliveries are reconciled against PO lines to detect missing shipments.
- Invoices are reconciled against PO totals to flag overcharges and billing variance.

#### 3.4 Multi-Target Engine Compatibility
- Seamless execution on local **DuckDB** (for instantaneous zero-configuration runs and unit tests).
- Ready for cloud/on-premise **PostgreSQL** data warehouses by adjusting `.env`.
