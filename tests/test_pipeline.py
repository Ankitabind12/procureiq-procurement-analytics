from pathlib import Path
import duckdb
import pytest

from src.config import DUCKDB_PATH, GOLD_EXPORTS_DIR
from src.ingestion.bronze_loader import BronzeLoader
from src.transformation.silver_transformer import SilverTransformer
from src.gold.gold_builder import GoldBuilder

def test_pipeline_idempotency():
    """Verify that running Bronze, Silver, and Gold transformations repeatedly yields deterministic row counts."""
    loader = BronzeLoader()
    counts_run1 = loader.load_all_bronze_tables()
    counts_run2 = loader.load_all_bronze_tables()
    assert counts_run1 == counts_run2, "Bronze layer ingestion must be idempotent"

    transformer = SilverTransformer()
    silver_run1 = transformer.execute_transformations()
    silver_run2 = transformer.execute_transformations()
    assert silver_run1 == silver_run2, "Silver layer transformations must be idempotent"

    builder = GoldBuilder()
    gold_run1 = builder.build_gold_marts_and_schema()
    gold_run2 = builder.build_gold_marts_and_schema()
    assert gold_run1 == gold_run2, "Gold layer mart compilations must be idempotent"

def test_gold_marts_populated():
    """Verify all 7 Gold Marts contain data."""
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    marts = [
        "gold_vendor_scorecard",
        "gold_procurement_spend",
        "gold_delivery_performance",
        "gold_invoice_analysis",
        "gold_compliance_status",
        "gold_purchase_order_summary",
        "gold_category_performance"
    ]
    for mart in marts:
        count = con.execute(f"SELECT COUNT(*) FROM {mart}").fetchone()[0]
        assert count > 0, f"Gold mart {mart} must not be empty"
    con.close()

def test_powerbi_exports_exist():
    """Verify that export files are present in data/gold_exports/."""
    expected_exports = [
        "gold_vendor_scorecard.csv",
        "gold_procurement_spend.csv",
        "gold_delivery_performance.csv",
        "gold_invoice_analysis.csv",
        "gold_compliance_status.csv",
        "gold_purchase_order_summary.csv",
        "gold_category_performance.csv",
        "fact_purchase_orders.csv",
        "fact_deliveries.csv",
        "fact_invoices.csv",
        "dim_vendor.csv",
        "dim_product.csv",
        "dim_department.csv",
        "dim_date.csv",
        "dim_category.csv"
    ]
    for exp in expected_exports:
        target = GOLD_EXPORTS_DIR / exp
        assert target.exists(), f"Power BI export {target} must exist"
        assert target.stat().st_size > 0, f"Export file {target} must not be empty"
