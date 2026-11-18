# ProcureIQ: Entity-Relationship (ER) Diagram

The following Mermaid ER Diagram models the transactional operational entities of the ProcureIQ platform, illustrating primary keys (`PK`), foreign keys (`FK`), and relational cardinality.

```mermaid
erDiagram
    DEPARTMENTS ||--o{ PURCHASE_ORDERS : places
    CATEGORIES ||--o{ PRODUCTS : categorizes
    CATEGORIES ||--o{ VENDORS : classifies
    VENDORS ||--o{ PURCHASE_ORDERS : fulfills
    VENDORS ||--o{ VENDOR_COMPLIANCE : holds
    PURCHASE_ORDERS ||--|{ PURCHASE_ORDER_ITEMS : contains
    PRODUCTS ||--o{ PURCHASE_ORDER_ITEMS : specifies
    PURCHASE_ORDERS ||--o{ DELIVERIES : tracks
    PURCHASE_ORDERS ||--o{ INVOICES : bills
    VENDORS ||--o{ INVOICES : issues

    DEPARTMENTS {
        string department_id PK
        string department_name
        string cost_center
        numeric annual_budget
        string manager
    }

    CATEGORIES {
        string category_id PK
        string category_name
        string spend_tier
        string description
    }

    PRODUCTS {
        string product_id PK
        string product_name
        string category_id FK
        numeric standard_cost
        string uom
        date created_date
    }

    VENDORS {
        string vendor_id PK
        string vendor_name
        string primary_category_id FK
        string country
        string city
        string payment_terms
        string risk_rating
        string vendor_status
        date registration_date
    }

    VENDOR_COMPLIANCE {
        string compliance_id PK
        string vendor_id FK
        string document_type
        date issue_date
        date expiry_date
        string compliance_status
        int audit_score
        string auditor_name
    }

    PURCHASE_ORDERS {
        string po_id PK
        string vendor_id FK
        string department_id FK
        date order_date
        date promised_delivery_date
        string po_status
        string currency
        numeric total_po_amount
        string buyer_name
    }

    PURCHASE_ORDER_ITEMS {
        string line_item_id PK
        string po_id FK
        int line_number
        string product_id FK
        int quantity_ordered
        numeric unit_price
        numeric line_total_amount
    }

    DELIVERIES {
        string delivery_id PK
        string po_id FK
        string vendor_id FK
        date promised_delivery_date
        date actual_delivery_date
        int delay_days
        string delivery_status
        string quality_inspection_result
        numeric defect_rate_percentage
        string carrier_name
        string tracking_number
    }

    INVOICES {
        string invoice_id PK
        string po_id FK
        string vendor_id FK
        date invoice_date
        date payment_due_date
        numeric po_amount
        numeric invoice_amount
        numeric discrepancy_amount
        boolean is_discrepancy
        string discrepancy_reason
        string payment_status
    }
```
