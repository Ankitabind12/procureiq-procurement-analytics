import duckdb
import pytest
from src.config import DUCKDB_PATH

@pytest.fixture(scope="module")
def db_conn():
    conn = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield conn
    conn.close()

def test_ontime_delivery_rate_bounds(db_conn):
    """Ensure on-time delivery percentage is logically bounded between 0% and 100%."""
    ontime_pct = db_conn.execute("""
        SELECT ROUND(CAST(SUM(is_ontime) AS NUMERIC) / COUNT(delivery_id) * 100.0, 2)
        FROM silver_deliveries;
    """).fetchone()[0]
    assert 0.0 <= ontime_pct <= 100.0, f"On-time rate {ontime_pct} must be between 0% and 100%"
    assert ontime_pct > 70.0, f"On-time rate {ontime_pct} should reflect realistic enterprise benchmark (>70%)"

def test_po_status_distribution(db_conn):
    """Ensure PO status counts sum to 100% of PO total."""
    res = db_conn.execute("""
        SELECT 
            COUNT(po_id) AS total_pos,
            SUM(CASE WHEN po_status = 'Fulfilled' THEN 1 ELSE 0 END) AS fulfilled,
            SUM(CASE WHEN po_status = 'Partially Fulfilled' THEN 1 ELSE 0 END) AS partial,
            SUM(CASE WHEN po_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
            SUM(CASE WHEN po_status = 'Open' THEN 1 ELSE 0 END) AS open_pos
        FROM silver_purchase_orders;
    """).fetchone()

    total, fulfilled, partial, cancelled, open_pos = res
    assert fulfilled + partial + cancelled + open_pos == total, "PO statuses must sum to total POs"
    assert total >= 5000, "Must have at least 5000 POs"

def test_invoice_discrepancy_calculation(db_conn):
    """Ensure discrepancy amount is exactly (invoice_amount - po_amount)."""
    discrepancy_errors = db_conn.execute("""
        SELECT COUNT(*)
        FROM silver_invoices
        WHERE ABS(discrepancy_amount - (invoice_amount - po_amount)) > 0.01;
    """).fetchone()[0]
    assert discrepancy_errors == 0, "Invoice discrepancy amount must equal invoice_amount - po_amount"

def test_vendor_scorecard_pillars(db_conn):
    """Ensure all vendors in gold_vendor_scorecard have valid pillar scores and performance tiers."""
    invalid_rows = db_conn.execute("""
        SELECT COUNT(*)
        FROM gold_vendor_scorecard
        WHERE composite_performance_score IS NULL
           OR composite_performance_score <= 0
           OR vendor_performance_tier NOT IN (
               'Tier 1 - Strategic Partner',
               'Tier 2 - Preferred Supplier',
               'Tier 3 - Operational Supplier',
               'Tier 4 - High Risk / PIP Required'
           );
    """).fetchone()[0]
    assert invalid_rows == 0, "All vendors must have valid composite scores and recognized tiers"
