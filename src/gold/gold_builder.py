from pathlib import Path
import duckdb

from src.config import DUCKDB_PATH, BASE_DIR
from src.utils.logger import logger

class GoldBuilder:
    """
    Gold Layer Service:
    Compiles enterprise analytical marts, aggregates vendor scorecards,
    and establishes Star Schema dimension and fact tables/views.
    """

    def __init__(self, db_path: Path = DUCKDB_PATH):
        self.db_path = db_path

    def get_connection(self):
        return duckdb.connect(str(self.db_path))

    def build_gold_marts_and_schema(self) -> dict:
        logger.info("Starting Gold Layer Modeling & Analytical Mart Compilation...")
        con = self.get_connection()

        gold_marts = [
            "gold_vendor_scorecard",
            "gold_procurement_spend",
            "gold_delivery_performance",
            "gold_invoice_analysis",
            "gold_compliance_status",
            "gold_purchase_order_summary",
            "gold_category_performance"
        ]

        # Drop existing gold marts for clean idempotent execution
        for mart in gold_marts:
            con.execute(f"DROP TABLE IF EXISTS {mart}")

        # Execute Gold Marts DDL
        gold_sql_path = BASE_DIR / "sql" / "03_gold_marts.sql"
        if not gold_sql_path.exists():
            raise FileNotFoundError(f"Missing gold script: {gold_sql_path}")
        con.execute(gold_sql_path.read_text(encoding="utf-8"))
        logger.info("Executed 03_gold_marts.sql successfully.")

        # Execute Star Schema Views
        star_sql_path = BASE_DIR / "sql" / "04_star_schema_views.sql"
        if not star_sql_path.exists():
            raise FileNotFoundError(f"Missing star schema script: {star_sql_path}")
        con.execute(star_sql_path.read_text(encoding="utf-8"))
        logger.info("Executed 04_star_schema_views.sql successfully.")

        mart_counts = {}
        for mart in gold_marts:
            count = con.execute(f"SELECT COUNT(*) FROM {mart}").fetchone()[0]
            mart_counts[mart] = count
            logger.info("Compiled Gold Mart '%s': %d records", mart, count)

        # Star schema views verification
        views = ["dim_vendor", "dim_product", "dim_department", "dim_date", "dim_category", "fact_purchase_orders", "fact_deliveries", "fact_invoices"]
        for v in views:
            v_count = con.execute(f"SELECT COUNT(*) FROM {v}").fetchone()[0]
            mart_counts[v] = v_count
            logger.info("Verified Star Schema View '%s': %d rows", v, v_count)

        con.close()
        logger.info("Gold Layer and Star Schema Modeling Completed: %s", mart_counts)
        return mart_counts

if __name__ == "__main__":
    builder = GoldBuilder()
    builder.build_gold_marts_and_schema()
