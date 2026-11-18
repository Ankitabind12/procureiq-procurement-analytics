# ProcureIQ: Quality Assurance & Testing Documentation

---

### 1. Testing Philosophy & Scope
To ensure that ProcureIQ meets production enterprise standards, data quality assertions and unit tests are embedded throughout the pipeline lifecycle:
- **Source Data Ingestion Testing**: Verifies schema conformances, non-empty primary keys, and source file existence.
- **Silver Referential Integrity Testing**: Validates that all transactional foreign keys map to existing dimensions with zero orphaned records.
- **Gold Mart Mathematical Testing**: Confirms mathematical boundaries (percentages between 0% and 100%, non-negative spend values).
- **Pipeline Idempotency Testing**: Executes sequential pipeline runs to prove that data states remain deterministic without duplicate record creation.
- **Power BI Export Verification**: Ensures all 15 business-ready CSV files are generated with valid row counts.

---

### 2. Automated Test Suite (Pytest)
The test suite is structured into three dedicated modules under `tests/`:

```
tests/
├── test_data_integrity.py      <- Foreign keys, null checks, positive quantities
├── test_kpi_calculations.py   <- KPI boundaries, status distributions, 4-pillar scores
└── test_pipeline.py           <- End-to-end idempotency & export verifications
```

#### Test Execution Summary:
```
tests/test_data_integrity.py::test_vendor_dimension_integrity PASSED          [ 9%]
tests/test_data_integrity.py::test_purchase_order_referential_integrity PASSED [18%]
tests/test_data_integrity.py::test_line_items_integrity PASSED                [27%]
tests/test_data_integrity.py::test_deliveries_and_invoices_linkage PASSED      [36%]
tests/test_kpi_calculations.py::test_ontime_delivery_rate_bounds PASSED       [45%]
tests/test_kpi_calculations.py::test_po_status_distribution PASSED            [54%]
tests/test_kpi_calculations.py::test_invoice_discrepancy_calculation PASSED  [63%]
tests/test_kpi_calculations.py::test_vendor_scorecard_pillars PASSED          [72%]
tests/test_pipeline.py::test_pipeline_idempotency PASSED                      [81%]
tests/test_pipeline.py::test_gold_marts_populated PASSED                      [90%]
tests/test_pipeline.py::test_powerbi_exports_exist PASSED                     [100%]

======================== 11 passed in 3.13s ========================
```

---

### 3. Test Cases Catalog

| Test Function | Target Module | Test Assertion | Business Risk Mitigated |
|---|---|---|---|
| `test_vendor_dimension_integrity` | `silver_vendors` | Vendor count &ge; 500, unique `vendor_id`, non-null names and categories. | Prevents missing vendor profiles and duplicate supplier entities. |
| `test_purchase_order_referential_integrity` | `silver_purchase_orders` | 100% of POs link to valid vendors in `silver_vendors` and departments in `silver_departments`. | Eliminates orphaned purchase orders in reporting. |
| `test_line_items_integrity` | `silver_purchase_order_items`| Line item count &ge; 8,000; quantities, unit prices, and totals strictly > 0. | Prevents negative or corrupted financial postings. |
| `test_deliveries_and_invoices_linkage` | `silver_deliveries`, `silver_invoices` | All shipments and billing invoices reference valid existing purchase orders. | Guarantees auditable 3-way matching between PO, receiving, and billing. |
| `test_ontime_delivery_rate_bounds` | `silver_deliveries` | On-time delivery rate is mathematically bounded between 0.0% and 100.0%. | Guarantees reliability formula precision. |
| `test_po_status_distribution` | `silver_purchase_orders` | `Fulfilled + Partial + Cancelled + Open == Total POs`. | Prevents unhandled lifecycle states in pipeline. |
| `test_invoice_discrepancy_calculation` | `silver_invoices` | Discrepancy amount strictly equals `(invoice_amount - po_amount)`. | Asserts accurate dollar calculations for AP overcharges. |
| `test_vendor_scorecard_pillars` | `gold_vendor_scorecard` | All composite scores are > 0 and assigned to recognized strategic tiers. | Guarantees valid executive supplier rankings. |
| `test_pipeline_idempotency` | Full Pipeline | Consecutive runs of loader, transformer, and builder produce identical row counts. | Eliminates accidental duplicate rows upon pipeline re-runs. |
| `test_gold_marts_populated` | Gold Marts | All 7 Gold Marts contain non-zero record counts. | Ensures reporting views are fully compiled. |
| `test_powerbi_exports_exist` | `data/gold_exports/` | All 15 export CSV files exist and contain non-empty data. | Guarantees Power BI readiness. |

---

### 4. Running the Tests Locally
Run all tests with detailed verbosity:
```bash
pytest -v
```

Run with test failure stop (`-x`):
```bash
pytest -x -v
```
