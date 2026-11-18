# ProcureIQ: Key Performance Indicator (KPI) Dictionary

---

### Master Procurement KPI Catalog

| KPI # | KPI Name | Mathematical Formula | Business Definition | Target SLA / Benchmark | Primary Stakeholder |
|---|---|---|---|---|---|
| **KPI-01** | **Total Procurement Spend** | $$\sum \text{PO Line Total Amount}$$ | Aggregate monetary volume committed across all executed purchase orders over the reporting period. | Within allocated fiscal budget | Chief Procurement Officer, CFO |
| **KPI-02** | **Vendor On-Time Delivery Rate** | $$\frac{\sum \text{On-Time Deliveries}}{\sum \text{Total Deliveries}} \times 100$$ | Percentage of shipments received at warehouse docks on or before the agreed contractual promised date. | &ge; 88.0% | VP Supply Chain, Logistics Lead |
| **KPI-03** | **Average Delivery Delay** | $$\frac{\sum \text{Delay Days}}{\sum \text{Total Deliveries}}$$ | Mean number of elapsed calendar days past promised delivery date across all incoming shipments. | &le; 1.5 Days | Logistics Operations |
| **KPI-04** | **PO Fulfilment Rate** | $$\frac{\sum \text{Fulfilled POs}}{\sum \text{Total POs Placed}} \times 100$$ | Proportion of placed purchase orders successfully completed without premature termination or cancellation. | &ge; 75.0% | Procurement Operations |
| **KPI-05** | **Invoice Discrepancy Rate** | $$\frac{\sum \text{Discrepant Invoices}}{\sum \text{Total Invoices Received}} \times 100$$ | Percentage of supplier invoices failing automated 3-way matching due to price variance, quantity mismatch, or overbilling. | &le; 10.0% | Accounts Payable Lead, Internal Audit |
| **KPI-06** | **Vendor Compliance Rate** | $$\frac{\sum \text{Compliant Certificates}}{\sum \text{Total Certificates On File}} \times 100$$ | Percentage of vendors maintaining active, unexpired regulatory, environmental, and liability insurance documentation. | &ge; 90.0% | Chief Compliance Officer, Legal Counsel |
| **KPI-07** | **Average Purchase Cost** | $$\frac{\text{Total Spend}}{\text{Total PO Count}}$$ and $$\text{AVG}(\text{Unit Price})$$ | Baseline benchmark cost per executed purchase order and mean unit acquisition cost per SKU. | Baseline monitoring | Category Sourcing Managers |
| **KPI-08** | **Department-wise Spend Share** | $$\frac{\text{Spend}_{\text{Dept}}}{\text{Total Spend}} \times 100$$ | Relative distribution of total corporate capital expended by internal business units and cost centers. | Budget alignment | Financial Planning & Analysis (FP&A) |
| **KPI-09** | **Vendor Performance Score** | $$0.35(D) + 0.25(P) + 0.25(Q) + 0.15(C)$$ | Balanced 4-pillar index evaluating Delivery ($D$), Price Competitiveness ($P$), Quality ($Q$), and Compliance ($C$). | &ge; 80.0 / 100 | Strategic Sourcing Committee |
| **KPI-10** | **PO Cancellation Rate** | $$\frac{\sum \text{Cancelled POs}}{\sum \text{Total POs Placed}} \times 100$$ | Percentage of generated purchase orders aborted due to vendor stockouts, obsolete requisitions, or administrative errors. | &le; 8.0% | Operations Director |

---

### Detailed 4-Pillar Scorecard Algorithm (KPI-09)
Suppliers are graded on an empirical 100-point composite scale to ensure objective contract awards and Performance Improvement Plan (PIP) enforcement:

1. **Delivery Reliability (35% Weight)**:
   $$\text{Score}_{\text{Delivery}} = \text{On-Time Delivery Rate \%} \times 0.35$$
2. **Price Competitiveness (25% Weight)**:
   $$\text{Score}_{\text{Price}} = \max\left(0, \left(2.0 - \frac{\text{Actual Paid Unit Price}}{\text{Standard Unit Benchmark}}\right) \times 100 \times 0.25\right)$$
3. **Product Quality (25% Weight)**:
   $$\text{Score}_{\text{Quality}} = \left(\frac{\text{Shipments Passing QC}}{\text{Total Shipments}}\right) \times 100 \times 0.25$$
4. **Documentation Compliance (15% Weight)**:
   $$\text{Score}_{\text{Compliance}} = \text{Audit Score (0-100)} \times 0.15$$

#### Strategic Classification Tiers:
- **Tier 1 (Score &ge; 88)**: Strategic Preferred Partner (Eligible for multi-year contract renewals and volume discounts).
- **Tier 2 (Score 75 - 87.9)**: Reliable Operational Supplier (Maintains healthy baseline fulfillment).
- **Tier 3 (Score 60 - 74.9)**: Monitored Supplier (Exhibits minor delivery or pricing volatility).
- **Tier 4 (Score < 60)**: High Risk / Mandatory PIP (Subject to order volume throttling or vendor phase-out).
