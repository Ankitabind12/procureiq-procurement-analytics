from pathlib import Path
import duckdb

from src.config import DUCKDB_PATH, BASE_DIR
from src.utils.logger import logger

class SilverTransformer:
    """
    Silver Layer Transformation Service:
    Applies data quality rules, deduplication, type casting, date normalization,
    and operational indicator derivations to Bronze records.
    """

    def __init__(self, db_path: Path = DUCKDB_PATH):
        self.db_path = db_path

    def get_connection(self):
        return duckdb.connect(str(self.db_path))

    def execute_transformations(self) -> dict:
        logger.info("Starting Silver Layer Transformations...")
        con = self.get_connection()

        silver_tables = [
            "silver_departments",
            "silver_categories",
            "silver_products",
            "silver_date_dimension",
            "silver_vendors",
            "silver_vendor_compliance",
            "silver_purchase_orders",
            "silver_purchase_order_items",
            "silver_deliveries",
            "silver_invoices"
        ]

        # Drop existing silver tables for clean idempotent re-run
        for tbl in silver_tables:
            con.execute(f"DROP TABLE IF EXISTS {tbl}")

        # Execute Silver SQL transformations
        sql_path = BASE_DIR / "sql" / "02_silver_transformations.sql"
        if not sql_path.exists():
            raise FileNotFoundError(f"Missing transformation script: {sql_path}")

        transformation_sql = sql_path.read_text(encoding="utf-8")
        con.execute(transformation_sql)
        logger.info("Executed 02_silver_transformations.sql successfully.")

        counts = {}
        for tbl in silver_tables:
            res = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            counts[tbl] = res
            logger.info("Created Silver table '%s': %d verified records", tbl, res)

        con.close()
        logger.info("Silver Layer Transformations Completed: %s", counts)
        return counts

if __name__ == "__main__":
    transformer = SilverTransformer()
    transformer.execute_transformations()
