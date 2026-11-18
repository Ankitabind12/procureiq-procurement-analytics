from pathlib import Path
import duckdb
import pandas as pd

from src.config import DUCKDB_PATH, GOLD_EXPORTS_DIR
from src.utils.logger import logger

def export_powerbi_datasets():
    """
    Exports all Gold Analytical Marts and Star Schema Dimensions & Facts
    to CSV format in data/gold_exports/ for seamless Power BI consumption.
    """
    logger.info("Exporting Business-Ready Datasets for Power BI...")
    con = duckdb.connect(str(DUCKDB_PATH))

    entities = [
        # Gold Business Marts
        "gold_vendor_scorecard",
        "gold_procurement_spend",
        "gold_delivery_performance",
        "gold_invoice_analysis",
        "gold_compliance_status",
        "gold_purchase_order_summary",
        "gold_category_performance",
        # Star Schema Dimensions & Facts
        "dim_vendor",
        "dim_product",
        "dim_department",
        "dim_date",
        "dim_category",
        "fact_purchase_orders",
        "fact_deliveries",
        "fact_invoices"
    ]

    export_summary = {}

    for entity in entities:
        df = con.execute(f"SELECT * FROM {entity}").fetchdf()
        out_csv = GOLD_EXPORTS_DIR / f"{entity}.csv"
        df.to_csv(out_csv, index=False)
        export_summary[entity] = len(df)
        logger.info("Exported '%s' (%d rows) -> %s", entity, len(df), out_csv)

    con.close()
    logger.info("Power BI Dataset Export Completed Successfully: %s", export_summary)
    return export_summary

if __name__ == "__main__":
    export_powerbi_datasets()
