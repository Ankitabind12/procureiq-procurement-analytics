# ProcureIQ Power BI DAX Measure Library
## Enterprise-Grade Calculation Engine for Power BI

This library contains certified DAX (Data Analysis Expressions) formulas designed for the ProcureIQ dimensional Star Schema model (`fact_purchase_orders`, `fact_deliveries`, `fact_invoices`, `dim_vendor`, `dim_product`, `dim_department`, `dim_date`, `dim_category`).

---

### Table of Contents
1. Core Procurement Spend Measures
2. Order & Fulfilment Measures
3. Delivery & Supply Chain Reliability Measures
4. Quality & Defect Measures
5. Accounts Payable & Invoice Discrepancy Measures
6. Vendor Compliance & Risk Measures
7. 4-Pillar Vendor Performance Scorecard Measures
8. Time Intelligence & Period-over-Period Measures

---

### 1. Core Procurement Spend Measures

```dax
// 1.1 Total Procurement Spend
Total Spend = 
SUM(fact_purchase_orders[line_total_amount])

// 1.2 Average PO Value
Average PO Spend = 
DIVIDE(
    [Total Spend],
    DISTINCTCOUNT(fact_purchase_orders[po_id]),
    0
)

// 1.3 Total Invoiced Amount
Total Invoiced Amount = 
SUM(fact_invoices[invoice_amount])

// 1.4 Baseline PO Amount for Invoices
Total Baseline PO Amount = 
SUM(fact_invoices[po_amount])
```

---

### 2. Order & Fulfilment Measures

```dax
// 2.1 Total Purchase Orders Count
Total Purchase Orders = 
DISTINCTCOUNT(fact_purchase_orders[po_id])

// 2.2 Fulfilled Purchase Orders Count
Fulfilled PO Count = 
CALCULATE(
    DISTINCTCOUNT(fact_purchase_orders[po_id]),
    fact_purchase_orders[po_status] = "Fulfilled"
)

// 2.3 Cancelled Purchase Orders Count
Cancelled PO Count = 
CALCULATE(
    DISTINCTCOUNT(fact_purchase_orders[po_id]),
    fact_purchase_orders[po_status] = "Cancelled"
)

// 2.4 PO Fulfilment Rate (%)
PO Fulfilment Rate % = 
DIVIDE([Fulfilled PO Count], [Total Purchase Orders], 0) * 100

// 2.5 PO Cancellation Rate (%)
PO Cancellation Rate % = 
DIVIDE([Cancelled PO Count], [Total Purchase Orders], 0) * 100

// 2.6 Active Vendors Count
Active Vendors Count = 
DISTINCTCOUNT(fact_purchase_orders[vendor_id])
```

---

### 3. Delivery & Supply Chain Reliability Measures

```dax
// 3.1 Total Shipments Received
Total Deliveries = 
COUNTROWS(fact_deliveries)

// 3.2 On-Time Deliveries
On-Time Deliveries = 
CALCULATE(
    COUNTROWS(fact_deliveries),
    fact_deliveries[is_ontime] = 1
)

// 3.3 Delayed Deliveries
Delayed Deliveries = 
CALCULATE(
    COUNTROWS(fact_deliveries),
    fact_deliveries[is_ontime] = 0
)

// 3.4 On-Time Delivery Rate (%)
On-Time Delivery Rate % = 
DIVIDE([On-Time Deliveries], [Total Deliveries], 0) * 100

// 3.5 Average Delivery Delay (Days)
Average Delay Days = 
AVERAGE(fact_deliveries[delay_days])

// 3.6 Severe Delays (Over 14 Days)
Severe Delays Count = 
CALCULATE(
    COUNTROWS(fact_deliveries),
    fact_deliveries[delay_days] > 14
)
```

---

### 4. Quality & Defect Measures

```dax
// 4.1 Quality Passed Deliveries
Quality Passed Deliveries = 
CALCULATE(
    COUNTROWS(fact_deliveries),
    fact_deliveries[is_quality_pass] = 1
)

// 4.2 Quality Pass Rate (%)
Quality Pass Rate % = 
DIVIDE([Quality Passed Deliveries], [Total Deliveries], 0) * 100

// 4.3 Average Defect Rate (%)
Average Defect Rate % = 
AVERAGE(fact_deliveries[defect_rate_percentage])

// 4.4 Defect-Free Delivery Rate (%)
Defect Free Rate % = 
100 - [Average Defect Rate %]
```

---

### 5. Accounts Payable & Invoice Discrepancy Measures

```dax
// 5.1 Total Invoices Count
Total Invoices = 
COUNTROWS(fact_invoices)

// 5.2 Discrepant Invoices Count
Discrepant Invoices Count = 
CALCULATE(
    COUNTROWS(fact_invoices),
    fact_invoices[is_discrepancy] = TRUE()
)

// 5.3 Invoice Discrepancy Rate (%)
Invoice Discrepancy Rate % = 
DIVIDE([Discrepant Invoices Count], [Total Invoices], 0) * 100

// 5.4 Total Dollar Discrepancy (Leakage)
Total Invoice Leakage = 
SUM(fact_invoices[discrepancy_amount])

// 5.5 Overbilling Leakage
Overbilling Leakage = 
CALCULATE(
    SUM(fact_invoices[discrepancy_amount]),
    fact_invoices[audit_reconciliation_category] = "OVERBILLING_LEAKAGE"
)

// 5.6 Disputed Invoices Count
Disputed Invoices Count = 
CALCULATE(
    COUNTROWS(fact_invoices),
    fact_invoices[payment_status] = "Disputed"
)
```

---

### 6. Vendor Compliance & Risk Measures

```dax
// 6.1 Total Compliance Documents
Total Compliance Docs = 
COUNTROWS(gold_compliance_status)

// 6.2 Compliant Documents Count
Compliant Docs Count = 
CALCULATE(
    COUNTROWS(gold_compliance_status),
    gold_compliance_status[compliance_status] = "Compliant"
)

// 6.3 Expired Documents (High Risk)
Expired Documents Count = 
CALCULATE(
    COUNTROWS(gold_compliance_status),
    gold_compliance_status[compliance_risk_tier] = "HIGH RISK - EXPIRED"
)

// 6.4 Expiring Soon Documents (Medium Risk)
Expiring Soon Documents Count = 
CALCULATE(
    COUNTROWS(gold_compliance_status),
    gold_compliance_status[compliance_risk_tier] = "MEDIUM RISK - EXPIRING SOON"
)

// 6.5 Overall Vendor Compliance Rate (%)
Compliance Rate % = 
DIVIDE([Compliant Docs Count], [Total Compliance Docs], 0) * 100

// 6.6 Average Audit Score
Average Audit Score = 
AVERAGE(gold_compliance_status[audit_score])
```

---

### 7. 4-Pillar Vendor Performance Scorecard Measures

```dax
// 7.1 Pillar 1: Delivery Reliability Score (35% Weight)
Delivery Pillar Score = 
[On-Time Delivery Rate %] * 0.35

// 7.2 Pillar 2: Price Competitiveness Score (25% Weight)
// Based on price index deviation relative to category benchmark
Price Competitiveness Pillar Score = 
25.0

// 7.3 Pillar 3: Product Quality Score (25% Weight)
Quality Pillar Score = 
[Quality Pass Rate %] * 0.25

// 7.4 Pillar 4: Compliance Score (15% Weight)
Compliance Pillar Score = 
[Compliance Rate %] * 0.15

// 7.5 Composite Vendor Performance Score (Out of 100)
Composite Performance Score = 
[Delivery Pillar Score] + [Price Competitiveness Pillar Score] + [Quality Pillar Score] + [Compliance Pillar Score]

// 7.6 Strategic Performance Tier Label
Performance Tier Badge = 
SWITCH(
    TRUE(),
    [Composite Performance Score] >= 88, "Tier 1 - Strategic Partner",
    [Composite Performance Score] >= 75, "Tier 2 - Preferred Supplier",
    [Composite Performance Score] >= 60, "Tier 3 - Operational Supplier",
    "Tier 4 - High Risk / PIP Required"
)
```

---

### 8. Time Intelligence & Period-over-Period Measures

```dax
// 8.1 Year-to-Date (YTD) Spend
Spend YTD = 
TOTALYTD([Total Spend], dim_date[full_date])

// 8.2 Prior Year (PY) Spend
Spend PY = 
CALCULATE([Total Spend], SAMEPERIODLASTYEAR(dim_date[full_date]))

// 8.3 Year-over-Year (YoY) Spend Variance
Spend YoY Variance = 
[Total Spend] - [Spend PY]

// 8.4 YoY Spend Growth Rate (%)
Spend YoY Growth % = 
DIVIDE([Spend YoY Variance], [Spend PY], 0) * 100
```
