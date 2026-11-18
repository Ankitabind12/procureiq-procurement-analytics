# ProcureIQ: End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Sources["1. Operational Source Layer"]
        S1["ERP Purchase Orders\n(5,000+ POs, 9,000+ Items)"]
        S2["Warehouse Receiving Dock\n(5,000+ Delivery Inspections)"]
        S3["Accounts Payable Billing\n(5,000+ Invoices)"]
        S4["Vendor & Compliance Master\n(500+ Suppliers, 500+ Certs)"]
    end

    subgraph Ingestion["2. Ingestion & Audit Layer"]
        P1["Python Bronze Loader\n(src/ingestion/bronze_loader.py)"]
        P1 -->|"Appends Metadata\n(_ingested_at, _source_file, _batch_id)"| B_DB
    end

    subgraph Warehouse["3. Medallion Data Warehouse (PostgreSQL / DuckDB)"]
        subgraph Bronze["Bronze Layer (Raw Ingestion)"]
            B_DB["bronze_purchase_orders\nbronze_purchase_order_items\nbronze_deliveries\nbronze_invoices\nbronze_vendors\nbronze_vendor_compliance"]
        end

        subgraph Silver["Silver Layer (Cleansing & Standardization)"]
            S_DB["silver_purchase_orders\nsilver_deliveries (delay tags)\nsilver_invoices (leakage flags)\nsilver_vendors (deduped)\nsilver_vendor_compliance (risk tiers)"]
        end

        subgraph Gold["Gold Layer (Business Marts & Star Schema)"]
            G1["gold_vendor_scorecard (4-Pillar Scores)"]
            G2["gold_procurement_spend (Monthly Trends)"]
            G3["gold_delivery_performance (Logistics)"]
            G4["gold_invoice_analysis (AP Discrepancies)"]
            G5["gold_compliance_status (Cert Expiries)"]
            G6["gold_purchase_order_summary"]
            G7["gold_category_performance"]
            F_DIM["Star Schema Facts & Conformed Dims\n(fact_pos, fact_deliveries, fact_invoices,\ndim_vendor, dim_product, dim_dept, dim_date)"]
        end

        Bronze -->|"Silver Transformations (sql/02_silver_transformations.sql)"| Silver
        Silver -->|"Gold Modeling & Aggregations (sql/03_gold_marts.sql)"| Gold
    end

    subgraph Analytics["4. Analytics & AI Engine"]
        A1["KPI Engine\n(10 Core Procurement KPIs)"]
        A2["Statistical Anomaly Detector\n(Z-Score Price Outliers & Chronic Delays)"]
    end

    subgraph Presentation["5. Executive BI Presentation"]
        BI1["Power BI Semantic Model\n(Certified DAX Measures)"]
        BI2["Interactive HTML Executive Dashboard\n(5-Page Procurement Intelligence)"]
    end

    Sources --> Ingestion
    Gold --> Analytics
    Gold --> Presentation
    Analytics --> Presentation
```

---

### Component Breakdown
1. **Operational Source Layer**: Simulates multi-system enterprise environments where POs originate in SAP/Oracle ERP, logistics events originate in warehouse management systems (WMS), and billing originates in accounts payable workflows.
2. **Ingestion & Audit Layer**: Python-powered batch loader that captures raw payloads, adds non-destructive audit stamps (`_ingested_at`, `_source_file`, `_batch_id`), and guarantees idempotent pipeline runs.
3. **Data Warehouse (Medallion Architecture)**:
   - **Bronze**: Exact replica of source CSV records.
   - **Silver**: Cleansed, deduplicated, type-cast tables with standardized date keys and referential integrity validations.
   - **Gold**: High-performance Star Schema dimensional models and aggregated domain marts.
4. **Analytics & AI Engine**: Automated engine that calculates transparent 4-pillar vendor performance ratings and statistical outlier detection.
5. **Presentation Layer**: Enterprise Power BI integration with certified DAX measures and browser-ready interactive dashboards.
