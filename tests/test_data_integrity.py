import duckdb
import pytest
from src.config import DUCKDB_PATH

@pytest.fixture(scope="module")
def db_conn():
    conn = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield conn
    conn.close()

def test_vendor_dimension_integrity(db_conn):
    """Ensure all vendors have unique IDs, valid names, and valid category foreign keys."""
    res = db_conn.execute("""
        SELECT 
            COUNT(vendor_id) AS total_vendors,
            COUNT(DISTINCT vendor_id) AS distinct_vendors,
            SUM(CASE WHEN vendor_name IS NULL OR vendor_name = '' THEN 1 ELSE 0 END) AS empty_names,
            SUM(CASE WHEN primary_category_id IS NULL THEN 1 ELSE 0 END) AS null_categories
        FROM silver_vendors;
    """).fetchone()

    total_vendors, distinct_vendors, empty_names, null_categories = res
    assert total_vendors >= 500, "Must have at least 500 vendors"
    assert total_vendors == distinct_vendors, "Vendor IDs must be unique"
    assert empty_names == 0, "Vendor names must not be empty"
    assert null_categories == 0, "Vendors must have assigned categories"

def test_purchase_order_referential_integrity(db_conn):
    """Ensure all POs link to valid vendors and valid departments."""
    unmatched_vendors = db_conn.execute("""
        SELECT COUNT(*) 
        FROM silver_purchase_orders po
        LEFT JOIN silver_vendors v ON po.vendor_id = v.vendor_id
        WHERE v.vendor_id IS NULL;
    """).fetchone()[0]
    assert unmatched_vendors == 0, "All POs must reference valid vendors"

    unmatched_depts = db_conn.execute("""
        SELECT COUNT(*) 
        FROM silver_purchase_orders po
        LEFT JOIN silver_departments d ON po.department_id = d.department_id
        WHERE d.department_id IS NULL;
    """).fetchone()[0]
    assert unmatched_depts == 0, "All POs must reference valid departments"

def test_line_items_integrity(db_conn):
    """Ensure all line items link to valid POs and valid products with positive values."""
    res = db_conn.execute("""
        SELECT 
            COUNT(*) AS total_items,
            SUM(CASE WHEN quantity_ordered <= 0 THEN 1 ELSE 0 END) AS invalid_qty,
            SUM(CASE WHEN unit_price <= 0 THEN 1 ELSE 0 END) AS invalid_price,
            SUM(CASE WHEN line_total_amount <= 0 THEN 1 ELSE 0 END) AS invalid_total
        FROM silver_purchase_order_items;
    """).fetchone()

    total_items, invalid_qty, invalid_price, invalid_total = res
    assert total_items >= 8000, "Must have at least 8000 PO line items"
    assert invalid_qty == 0, "Quantities ordered must be strictly positive"
    assert invalid_price == 0, "Unit prices must be strictly positive"
    assert invalid_total == 0, "Line totals must be strictly positive"

def test_deliveries_and_invoices_linkage(db_conn):
    """Ensure deliveries and invoices reference valid purchase orders."""
    unmatched_deliveries = db_conn.execute("""
        SELECT COUNT(*) 
        FROM silver_deliveries d
        LEFT JOIN silver_purchase_orders po ON d.po_id = po.po_id
        WHERE po.po_id IS NULL;
    """).fetchone()[0]
    assert unmatched_deliveries == 0, "All deliveries must reference valid POs"

    unmatched_invoices = db_conn.execute("""
        SELECT COUNT(*) 
        FROM silver_invoices inv
        LEFT JOIN silver_purchase_orders po ON inv.po_id = po.po_id
        WHERE po.po_id IS NULL;
    """).fetchone()[0]
    assert unmatched_invoices == 0, "All invoices must reference valid POs"
