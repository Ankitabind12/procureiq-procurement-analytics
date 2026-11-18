# ProcureIQ Power BI Dashboard Design Guide
## Executive BI Design Specification & Layout Wireframes

---

### 1. Visual Theme & Corporate Palette
The ProcureIQ reporting suite adheres to modern enterprise executive aesthetics:
- **Primary Navy / Midnight Blue**: `#0F172A` (Headers, Primary Cards)
- **Accent Emerald Green (Positive / On-Time)**: `#10B981` (On-time, Quality Pass, Compliant)
- **Warning Amber (Attention / Pending)**: `#F59E0B` (Minor delay, Expiring soon, Pending review)
- **Critical Red (Risk / Discrepancy)**: `#EF4444` (Severe delay, Expired doc, Invoice leakage)
- **Slate Gray (Neutral Background)**: `#F8FAFC` (Canvas background)
- **Card Surface**: `#FFFFFF` with 1px border `#E2E8F0` and subtle drop-shadow.

---

### 2. PAGE 1: PROCUREMENT OVERVIEW
**Target Audience**: Chief Procurement Officer (CPO), VP Supply Chain, Financial Directors.  
**Core Goal**: Deliver immediate, high-level visibility into macro spend volume, vendor base health, and fulfillment trends.

#### Layout Wireframe
```
+-----------------------------------------------------------------------------------------+
| [LOGO] ProcureIQ Executive Overview   | Slicers: [Year v] [Quarter v] [Department v]     |
+-----------------------------------------------------------------------------------------+
| [ KPI CARD 1 ]     | [ KPI CARD 2 ]     | [ KPI CARD 3 ]    | [ KPI CARD 4 ]            |
| Total Spend        | Total Orders       | Active Vendors    | On-Time Delivery Rate %   |
| $556.52M           | 5,000 POs          | 500 Suppliers     | 87.14%                    |
+-----------------------------------------------------------------------------------------+
| [ AREA / LINE CHART ]                                  | [ DONUT / BAR CHART ]          |
| Monthly Procurement Spend Trajectory (2023 - 2025)     | Spend by Category Breakdown    |
| (Shows seasonality & budget exhaustion trends)         | (Raw Materials, Machinery, IT) |
+-----------------------------------------------------------------------------------------+
| [ HORIZONTAL BAR CHART ]                               | [ DONUT CHART ]                |
| Department-wise Procurement Spend & Budget Share       | Purchase Order Status Mix      |
| (Manufacturing vs Supply Chain vs IT vs R&D)           | (Fulfilled vs Cancelled vs O/S)|
+-----------------------------------------------------------------------------------------+
```

#### Visual Component Specifications
1. **Top KPI Ribbon**:
   - Card 1: `Total Spend` (`$556.52M`) with YoY growth indicator.
   - Card 2: `Total Purchase Orders` (`5,000`).
   - Card 3: `Active Vendors` (`500`).
   - Card 4: `On-Time Delivery Rate` (`87.14%`) with conditional green/red target gauge (Target >= 88%).
2. **Monthly Spend Trend**: Area chart with `dim_date[Year-Month]` on X-axis, `[Total Spend]` on Y-axis.
3. **Category-wise Spend**: Donut chart displaying share of spend across the 7 procurement categories.
4. **Department Spend Bar Chart**: Clustered horizontal bar comparing budget allocation vs actual spend.

---

### 3. PAGE 2: VENDOR PERFORMANCE SCORECARD
**Target Audience**: Strategic Sourcing Managers, Vendor Relationship Directors.  
**Core Goal**: Rank and objectively evaluate suppliers across the 4 core performance pillars.

#### Layout Wireframe
```
+-----------------------------------------------------------------------------------------+
| Vendor Performance & Sourcing Intelligence | Slicers: [Category v] [Tier v] [Vendor v]  |
+-----------------------------------------------------------------------------------------+
| [ KPI CARD 1 ]       | [ KPI CARD 2 ]     | [ KPI CARD 3 ]      | [ KPI CARD 4 ]        |
| Avg Vendor Score     | Tier-1 Partners    | Preferred Suppliers | High-Risk / PIP       |
| 82.4 / 100           | 142 Vendors        | 218 Vendors         | 34 Vendors            |
+-----------------------------------------------------------------------------------------+
| [ SCATTER PLOT / QUADRANT MATRIX ]                     | [ RADAR / 4-PILLAR BAR ]       |
| Vendor Delivery Reliability % (X) vs Quality Pass % (Y)| 4-Pillar Score Weights:        |
| Bubble Size = Total Spend Exposure                     | Reliability (35%) | Price (25%)|
| Quadrant 1 = Strategic Champions                       | Quality (25%)     | Compl (15%)|
+-----------------------------------------------------------------------------------------+
| [ INTERACTIVE VENDOR RANKING TABLE ]                                                    |
| Vendor Name | Category | Total Spend | On-Time % | Quality % | Score | Tier Classification|
| Apex Industries | Raw Mat | $2.4M   | 96.2%     | 98.5%     | 92.4  | [Tier 1 - Strategic]|
+-----------------------------------------------------------------------------------------+
```

#### Visual Component Specifications
1. **Performance Quadrant**: Scatter visual plotting `[On-Time Delivery Rate %]` on X-axis and `[Quality Pass Rate %]` on Y-axis.
2. **Scorecard Data Grid**: Matrix table featuring conditional formatting data bars for scores and colored badge pills for tiers.
3. **Pillar Breakdown**: Clustered bar chart showing how a selected vendor scores across Delivery (35%), Price (25%), Quality (25%), and Compliance (15%).

---

### 4. PAGE 3: DELIVERY & LOGISTICS ANALYTICS
**Target Audience**: Logistics Operations, Receiving Dock Supervisors, Category Managers.  
**Core Goal**: Track on-time fulfillment, diagnose transit bottlenecks, and evaluate freight carrier efficiency.

#### Layout Wireframe
```
+-----------------------------------------------------------------------------------------+
| Delivery & Logistics Analytics           | Slicers: [Carrier v] [Delay Bucket v] [Date v]|
+-----------------------------------------------------------------------------------------+
| [ KPI CARD 1 ]       | [ KPI CARD 2 ]     | [ KPI CARD 3 ]      | [ KPI CARD 4 ]        |
| Total Deliveries     | On-Time Shipments  | Delayed Shipments   | Avg Delivery Delay    |
| 5,000                | 4,357 (87.1%)      | 643 (12.9%)         | 0.99 Days             |
+-----------------------------------------------------------------------------------------+
| [ 100% STACKED BAR CHART ]                             | [ HEATMAP / DURATION BAR ]     |
| Monthly On-Time vs Delayed Delivery Proportion         | Delay Severity Distribution    |
| (Emerald = On-Time, Crimson = Delayed)                 | (1-7 Days, 8-14 Days, 15+ Days)|
+-----------------------------------------------------------------------------------------+
| [ CARRIER BENCHMARK TABLE ]                            | [ CHRONIC DELAY OFFENDERS ]    |
| Carrier Name | Shipments | On-Time % | Avg Delay Days  | Vendor Name | Delay Rate % | Spend|
| FedEx Freight| 1,024     | 89.2%     | 0.8 days        | Vanguard Ltd| 48.0%        | $1.8M|
+-----------------------------------------------------------------------------------------+
```

#### Visual Component Specifications
1. **On-Time vs Delay Distribution**: 100% stacked bar chart over calendar months illustrating trend towards operational delivery SLA.
2. **Delay Severity Buckets**: Bar chart categorizing delayed shipments into `1-7 Days`, `8-14 Days`, and `15+ Days Severe Delay`.
3. **Carrier Benchmark Grid**: Cross-tabulation of delivery performance across freight carriers (FedEx, DHL, Maersk, UPS, Schneider).

---

### 5. PAGE 4: INVOICE & SPENDING RECONCILIATION
**Target Audience**: Accounts Payable (AP) Lead, Internal Audit, Financial Controllers.  
**Core Goal**: Detect 3-way match failures, eliminate billing overcharges, and audit discrepancy leakage.

#### Layout Wireframe
```
+-----------------------------------------------------------------------------------------+
| Invoice & Accounts Payable Analytics     | Slicers: [Discrepancy Reason v] [Status v]   |
+-----------------------------------------------------------------------------------------+
| [ KPI CARD 1 ]       | [ KPI CARD 2 ]     | [ KPI CARD 3 ]      | [ KPI CARD 4 ]        |
| Total Invoices       | Discrepant Count   | Discrepancy Rate    | Financial Leakage     |
| 5,000                | 851 Invoices       | 17.02%              | $14,074,490.48        |
+-----------------------------------------------------------------------------------------+
| [ WATERFALL / DONUT CHART ]                            | [ SCATTER / COMPARISON CHART ] |
| Discrepancy Breakdown by Root Cause                    | Purchase Order Amount (X) vs   |
| (Price Variance vs Quantity Mismatch vs Overbilling)   | Invoiced Billed Amount (Y)     |
+-----------------------------------------------------------------------------------------+
| [ ACCOUNTS PAYABLE AUDIT DRILL-DOWN TABLE ]                                             |
| Invoice ID | PO ID | Vendor Name | PO Amount | Invoice Amount | Leakage ($) | Status     |
| INV-000412 | PO-001| Precision Co| $120,000  | $138,000       | +$18,000    | Disputed   |
+-----------------------------------------------------------------------------------------+
```

#### Visual Component Specifications
1. **Leakage KPI Banner**: Highlight `$14.07M` in invoice variance requiring immediate Accounts Payable credit notes or dispute resolutions.
2. **Variance Root Cause Donut**: Visual split between unit price variances, quantity deviations, and duplicate billings.
3. **PO vs Invoice Correlation Scatter Plot**: Highlights line items deviating above the 45-degree diagonal reference line (`y = x`).

---

### 6. PAGE 5: REGULATORY COMPLIANCE & RISK MONITORING
**Target Audience**: Compliance Officer, Legal Counsel, Procurement Risk Committee.  
**Core Goal**: Eliminate legal and supply chain liabilities caused by lapsed supplier certifications.

#### Layout Wireframe
```
+-----------------------------------------------------------------------------------------+
| Supplier Compliance & Risk Guardrails    | Slicers: [Risk Tier v] [Document Type v]     |
+-----------------------------------------------------------------------------------------+
| [ KPI CARD 1 ]       | [ KPI CARD 2 ]     | [ KPI CARD 3 ]      | [ KPI CARD 4 ]        |
| Total Certifications | Compliant (Valid)  | Expired (High Risk) | Expiring Soon (<45d)  |
| 500 Audits           | 398 (79.6%)        | 72 (14.4%)          | 30 (6.0%)             |
+-----------------------------------------------------------------------------------------+
| [ DONUT CHART ]                                        | [ STACKED BAR BY DOC TYPE ]    |
| Compliance Risk Tier Proportion                        | Expiry Breakdown by Certificate|
| (Low Risk Valid vs Medium Soon vs High Expired)        | (ISO 9001, Insurance, Tax)     |
+-----------------------------------------------------------------------------------------+
| [ HIGH-PRIORITY ACTION REQUIRED GRID ]                                                  |
| Vendor Name | Certificate Type | Expiry Date | Status | Audit Score | Action Plan       |
| Titan Supply| Comm. Insurance  | 2025-10-12  | Expired| 48 / 100    | [HOLD POs / AUDIT]|
+-----------------------------------------------------------------------------------------+
```

#### Visual Component Specifications
1. **Compliance Status Donut**: Green (Compliant), Amber (Expiring in <= 45 days), Red (Expired).
2. **Certificate Type Vulnerability Matrix**: Horizontal stacked bar displaying compliance health across ISO 9001, ISO 14001, ISO 27001, Commercial Liability Insurance, and Tax Clearances.
3. **Urgent Action Grid**: Pre-filtered to `HIGH RISK - EXPIRED` records with one-click action recommendations (`Immediate Stop-Shipment / Audit Required`).
