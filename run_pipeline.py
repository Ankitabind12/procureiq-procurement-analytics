#!/usr/bin/env python3
"""
=============================================================================
ProcureIQ: Master End-to-End ELT & Analytics Pipeline Runner
=============================================================================
Orchestrates the complete Medallion Architecture data engineering lifecycle:
1. Validates / Generates Realistic Synthetic Datasets
2. Loads Bronze Layer with Audit Stamping
3. Executes Silver Cleansing & Referential Integrity Transformations
4. Compiles Gold Analytical Marts & Star Schema Views
5. Computes Executive Procurement KPIs & Business Recommendations
6. Executes Statistical Anomaly & Risk Detection
7. Exports Business-Ready Datasets for Power BI Dashboard
=============================================================================
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.config import RAW_DATA_DIR
from src.utils.logger import logger
from src.generator.data_generator import generate_all_datasets
from src.ingestion.bronze_loader import BronzeLoader
from src.transformation.silver_transformer import SilverTransformer
from src.gold.gold_builder import GoldBuilder
from src.gold.kpi_engine import KPIEngine
from src.analytics.anomaly_detector import ProcurementAnomalyDetector
from power_bi.export_powerbi_data import export_powerbi_datasets

def run_master_pipeline():
    start_time = time.time()
    logger.info("======================================================================")
    logger.info("   PROCUREIQ: INTELLIGENT PROCUREMENT ANALYTICS PLATFORM (PIPELINE)   ")
    logger.info("======================================================================")

    # STEP 1: Verify or generate raw data
    required_raw_files = [
        "departments.csv", "categories.csv", "products.csv", "date_dimension.csv",
        "vendors.csv", "vendor_compliance.csv", "purchase_orders.csv",
        "purchase_order_items.csv", "deliveries.csv", "invoices.csv"
    ]
    missing_files = [f for f in required_raw_files if not (RAW_DATA_DIR / f).exists()]
    if missing_files:
        logger.info("Missing raw files detected: %s. Generating fresh datasets...", missing_files)
        generate_all_datasets()
    else:
        logger.info("Raw datasets verified in %s.", RAW_DATA_DIR)

    # STEP 2: Bronze Layer Ingestion
    logger.info("\n--- PHASE 1/6: BRONZE LAYER INGESTION ---")
    loader = BronzeLoader()
    bronze_counts = loader.load_all_bronze_tables()

    # STEP 3: Silver Layer Transformations
    logger.info("\n--- PHASE 2/6: SILVER LAYER TRANSFORMATIONS ---")
    transformer = SilverTransformer()
    silver_counts = transformer.execute_transformations()

    # STEP 4: Gold Layer Modeling & Star Schema
    logger.info("\n--- PHASE 3/6: GOLD LAYER ANALYTICAL MARTS ---")
    builder = GoldBuilder()
    gold_counts = builder.build_gold_marts_and_schema()

    # STEP 5: KPI Engine & Business Analysis
    logger.info("\n--- PHASE 4/6: EXECUTIVE KPI COMPUTATION ---")
    kpi_engine = KPIEngine()
    kpi_results = kpi_engine.compute_kpis()

    # STEP 6: Advanced Anomaly & Risk Detection
    logger.info("\n--- PHASE 5/6: STATISTICAL ANOMALY DETECTION ---")
    detector = ProcurementAnomalyDetector()
    anomaly_results = detector.run_full_anomaly_scan()

    # STEP 7: Export Power BI Ready Datasets
    logger.info("\n--- PHASE 6/6: POWER BI DATASET EXPORT ---")
    export_counts = export_powerbi_datasets()

    duration = round(time.time() - start_time, 2)
    logger.info("\n======================================================================")
    logger.info("   PROCUREIQ PIPELINE RUN SUCCESSFUL! (Duration: %s seconds)         ", duration)
    logger.info("======================================================================")
    logger.info("PIPELINE SUMMARY:")
    logger.info(" - Total Spend Processed:       $%s", f"{kpi_results['summary_kpis']['1_total_procurement_spend']:,.2f}")
    logger.info(" - PO Fulfilment Rate:          %s%%", kpi_results['summary_kpis']['4_po_fulfilment_rate_pct'])
    logger.info(" - On-Time Delivery Rate:       %s%%", kpi_results['summary_kpis']['2_vendor_ontime_delivery_rate_pct'])
    logger.info(" - Avg Delivery Delay:          %s days", kpi_results['summary_kpis']['3_avg_delivery_delay_days'])
    logger.info(" - Invoice Discrepancy Rate:    %s%%", kpi_results['summary_kpis']['5_invoice_discrepancy_rate_pct'])
    logger.info(" - Total Invoice Leakage:       $%s", f"{kpi_results['leakage_exposure']['total_leakage_dollars']:,.2f}")
    logger.info(" - Price Anomalies Flagged:     %d", anomaly_results['total_price_anomalies_flagged'])
    logger.info(" - Power BI Tables Exported:    %d", len(export_counts))
    logger.info("======================================================================\n")

    return {
        "bronze": bronze_counts,
        "silver": silver_counts,
        "gold": gold_counts,
        "kpi": kpi_results,
        "anomalies": anomaly_results,
        "exports": export_counts,
        "duration_sec": duration
    }

if __name__ == "__main__":
    run_master_pipeline()
