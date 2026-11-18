import datetime
import uuid
from pathlib import Path
import pandas as pd
import duckdb

from src.config import RAW_DATA_DIR, DUCKDB_PATH, BASE_DIR
from src.utils.logger import logger

class BronzeLoader:
    """
    Bronze Layer Ingestion Service:
    Ingests raw procurement CSV files into the Bronze Data Lakehouse / Warehouse layer,
    enriching each row with source audit metadata (_ingested_at, _source_file, _batch_id).
    """

    def __init__(self, db_path: Path = DUCKDB_PATH):
        self.db_path = db_path
        self.batch_id = f"BATCH-{datetime.date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"

    def get_connection(self):
        return duckdb.connect(str(self.db_path))

    def load_all_bronze_tables(self) -> dict:
        logger.info("Starting Bronze Layer Ingestion [Batch ID: %s]...", self.batch_id)
        con = self.get_connection()

        # DDL initialization
        ddl_path = BASE_DIR / "sql" / "01_bronze_ddl.sql"
        if ddl_path.exists():
            ddl_sql = ddl_path.read_text(encoding="utf-8")
            con.execute(ddl_sql)
            logger.info("Bronze schema DDL executed successfully.")

        tables = {
            "departments.csv": "bronze_departments",
            "categories.csv": "bronze_categories",
            "products.csv": "bronze_products",
            "date_dimension.csv": "bronze_date_dimension",
            "vendors.csv": "bronze_vendors",
            "vendor_compliance.csv": "bronze_vendor_compliance",
            "purchase_orders.csv": "bronze_purchase_orders",
            "purchase_order_items.csv": "bronze_purchase_order_items",
            "deliveries.csv": "bronze_deliveries",
            "invoices.csv": "bronze_invoices"
        }

        ingested_counts = {}
        ingest_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for csv_file, table_name in tables.items():
            csv_path = RAW_DATA_DIR / csv_file
            if not csv_path.exists():
                logger.warning("Source file %s not found. Skipping...", csv_path)
                continue

            df = pd.read_csv(csv_path)
            # Add Bronze operational audit columns
            df["_ingested_at"] = ingest_ts
            df["_source_file"] = csv_file
            df["_batch_id"] = self.batch_id

            # Register temporary view and insert/replace into Bronze table
            con.register("temp_df", df)
            con.execute(f"DROP TABLE IF EXISTS {table_name}")
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
            con.unregister("temp_df")

            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            ingested_counts[table_name] = count
            logger.info("Loaded Bronze table '%s': %d records", table_name, count)

        con.close()
        logger.info("Bronze Layer Ingestion Completed: %s", ingested_counts)
        return ingested_counts

if __name__ == "__main__":
    loader = BronzeLoader()
    loader.load_all_bronze_tables()
