# ProcureIQ: Dimensional Star Schema Architecture

```mermaid
flowchart TD
    subgraph Dimensions["Conformed Dimensions"]
        D_VEN["dim_vendor\n(PK: vendor_id)"]
        D_PRD["dim_product\n(PK: product_id)"]
        D_DEP["dim_department\n(PK: department_id)"]
        D_DAT["dim_date\n(PK: date_key YYYYMMDD)"]
        D_CAT["dim_category\n(PK: category_id)"]
    end

    subgraph Facts["Fact Tables (Core Business Events)"]
        F_PO["fact_purchase_orders\n(PK: line_item_id)\n-- Grain: One row per PO line item\n-- Measures: qty_ordered, unit_price, line_total_amount"]
        F_DEL["fact_deliveries\n(PK: delivery_id)\n-- Grain: One row per receiving shipment\n-- Measures: delay_days, defect_rate_percentage, is_ontime"]
        F_INV["fact_invoices\n(PK: invoice_id)\n-- Grain: One row per vendor billing invoice\n-- Measures: po_amount, invoice_amount, discrepancy_amount"]
    end

    %% Fact PO Relationships
    D_VEN -->|1 : N| F_PO
    D_PRD -->|1 : N| F_PO
    D_DEP -->|1 : N| F_PO
    D_DAT -->|1 : N (order_date_key)| F_PO

    %% Fact Deliveries Relationships
    D_VEN -->|1 : N| F_DEL
    D_DAT -->|1 : N (actual_date_key)| F_DEL

    %% Fact Invoices Relationships
    D_VEN -->|1 : N| F_INV
    D_DAT -->|1 : N (invoice_date_key)| F_INV

    %% Outrigger / Snowflaking for categories
    D_CAT -->|1 : N| D_VEN
    D_CAT -->|1 : N| D_PRD
```

---

### Fact Table Granularity Definitions
1. **`fact_purchase_orders`**:
   - **Grain**: Exactly one line item of a purchase order (`line_item_id`).
   - **Foreign Keys**: `vendor_id`, `product_id`, `department_id`, `order_date_key`, `promised_date_key`.
   - **Degenerate Dimensions**: `po_id`, `buyer_name`, `po_status`.
   - **Additive Measures**: `quantity_ordered`, `line_total_amount`.
2. **`fact_deliveries`**:
   - **Grain**: Exactly one shipment event received at dock (`delivery_id`).
   - **Foreign Keys**: `po_id`, `vendor_id`, `actual_delivery_date_key`.
   - **Degenerate Dimensions**: `carrier_name`, `tracking_number`, `delivery_status`, `quality_inspection_result`.
   - **Additive Measures**: `delay_days`, `defect_rate_percentage`, `is_ontime` (semi-additive).
3. **`fact_invoices`**:
   - **Grain**: Exactly one vendor billing invoice (`invoice_id`).
   - **Foreign Keys**: `po_id`, `vendor_id`, `invoice_date_key`.
   - **Degenerate Dimensions**: `discrepancy_reason`, `payment_status`, `audit_reconciliation_category`.
   - **Additive Measures**: `po_amount`, `invoice_amount`, `discrepancy_amount`.
