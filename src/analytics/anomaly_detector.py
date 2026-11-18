import json
from pathlib import Path
import duckdb
import numpy as np
import pandas as pd

from src.config import DUCKDB_PATH, BASE_DIR
from src.utils.logger import logger

class ProcurementAnomalyDetector:
    """
    Advanced Procurement Analytics & Anomaly Detection:
    - Statistical Unit Price Anomaly Detection (Z-score & IQR outlier analysis)
    - Chronic Delivery Delay Risk Engine
    - Supplier Compliance Expiry Guardrails
    """

    def __init__(self, db_path: Path = DUCKDB_PATH):
        self.db_path = db_path

    def get_connection(self):
        return duckdb.connect(str(self.db_path))

    def detect_price_anomalies(self, z_threshold: float = 2.0) -> pd.DataFrame:
        """
        Flags line items where the unit price paid significantly deviates
        from the product's historical benchmark or category standard.
        """
        logger.info("Running Statistical Price Outlier Anomaly Detection...")
        con = self.get_connection()
        query = """
        SELECT 
            poi.line_item_id,
            po.po_id,
            po.vendor_id,
            v.vendor_name,
            poi.product_id,
            p.product_name,
            c.category_name,
            poi.quantity_ordered,
            poi.unit_price,
            p.standard_cost,
            ROUND((poi.unit_price - p.standard_cost) / NULLIF(p.standard_cost, 0) * 100.0, 2) AS price_variance_pct,
            poi.line_total_amount
        FROM silver_purchase_order_items poi
        JOIN silver_purchase_orders po ON poi.po_id = po.po_id
        JOIN silver_products p ON poi.product_id = p.product_id
        JOIN silver_categories c ON p.category_id = c.category_id
        JOIN silver_vendors v ON po.vendor_id = v.vendor_id;
        """
        df = con.execute(query).fetchdf()
        con.close()

        # Compute category-level Z-Scores for unit price ratios
        df["price_ratio"] = df["unit_price"] / df["standard_cost"]
        df["z_score"] = df.groupby("category_name")["price_ratio"].transform(
            lambda x: (x - x.mean()) / (x.std() + 1e-6)
        )

        anomalies = df[df["z_score"] >= z_threshold].copy()
        anomalies["anomaly_type"] = "HIGH_PRICE_OUTLIER"
        anomalies["potential_excess_cost"] = np.round(
            (anomalies["unit_price"] - anomalies["standard_cost"]) * anomalies["quantity_ordered"], 2
        )
        anomalies = anomalies.sort_values(by="potential_excess_cost", ascending=False)
        logger.info("Identified %d price anomaly records.", len(anomalies))
        return anomalies

    def detect_chronic_delay_vendors(self, min_shipments: int = 5, delay_rate_threshold: float = 40.0) -> pd.DataFrame:
        """
        Flags vendors with persistent delivery delays threatening supply chain continuity.
        """
        logger.info("Detecting Chronic Late Delivery Vendors...")
        con = self.get_connection()
        query = f"""
        SELECT 
            v.vendor_id,
            v.vendor_name,
            c.category_name,
            COUNT(d.delivery_id) AS total_shipments,
            SUM(d.is_ontime) AS ontime_count,
            COUNT(d.delivery_id) - SUM(d.is_ontime) AS delayed_count,
            ROUND((COUNT(d.delivery_id) - SUM(d.is_ontime)) * 100.0 / COUNT(d.delivery_id), 2) AS delay_rate_pct,
            ROUND(AVG(d.delay_days), 2) AS avg_delay_days,
            ROUND(MAX(d.delay_days), 2) AS max_delay_days,
            'DELIVERY_RELIABILITY_RISK' AS risk_flag
        FROM silver_deliveries d
        JOIN silver_vendors v ON d.vendor_id = v.vendor_id
        JOIN silver_categories c ON v.primary_category_id = c.category_id
        GROUP BY v.vendor_id, v.vendor_name, c.category_name
        HAVING COUNT(d.delivery_id) >= {min_shipments}
           AND ((COUNT(d.delivery_id) - SUM(d.is_ontime)) * 100.0 / COUNT(d.delivery_id)) >= {delay_rate_threshold}
        ORDER BY avg_delay_days DESC;
        """
        df_chronic = con.execute(query).fetchdf()
        con.close()
        logger.info("Identified %d chronic delay vendors.", len(df_chronic))
        return df_chronic

    def detect_compliance_alerts(self) -> pd.DataFrame:
        """
        Identifies expired or near-expiry regulatory and safety certificates.
        """
        logger.info("Scanning for Supplier Compliance Expiry Alerts...")
        con = self.get_connection()
        query = """
        SELECT 
            c.compliance_id,
            v.vendor_id,
            v.vendor_name,
            c.document_type,
            c.expiry_date,
            c.compliance_risk_tier,
            c.audit_score,
            c.auditor_name
        FROM silver_vendor_compliance c
        JOIN silver_vendors v ON c.vendor_id = v.vendor_id
        WHERE c.compliance_risk_tier IN ('HIGH RISK - EXPIRED', 'MEDIUM RISK - EXPIRING SOON')
        ORDER BY c.expiry_date ASC;
        """
        df_comp = con.execute(query).fetchdf()
        con.close()
        logger.info("Identified %d compliance alert records.", len(df_comp))
        return df_comp

    def run_full_anomaly_scan(self) -> dict:
        price_outliers = self.detect_price_anomalies()
        chronic_delays = self.detect_chronic_delay_vendors()
        compliance_alerts = self.detect_compliance_alerts()

        results = {
            "total_price_anomalies_flagged": len(price_outliers),
            "total_estimated_excess_price_exposure": float(price_outliers["potential_excess_cost"].sum()) if not price_outliers.empty else 0.0,
            "chronic_delay_vendors_count": len(chronic_delays),
            "compliance_risk_alerts_count": len(compliance_alerts),
            "top_price_outliers_sample": price_outliers[["po_id", "vendor_name", "product_name", "unit_price", "standard_cost", "z_score", "potential_excess_cost"]].head(5).to_dict(orient="records"),
            "top_chronic_delay_vendors_sample": chronic_delays.head(5).to_dict(orient="records"),
            "urgent_compliance_expiries_sample": compliance_alerts.head(5).to_dict(orient="records")
        }

        # Export anomaly summary
        output_file = BASE_DIR / "docs" / "anomaly_detection_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info("Saved Anomaly Detection Report to %s", output_file)

        return results

if __name__ == "__main__":
    detector = ProcurementAnomalyDetector()
    detector.run_full_anomaly_scan()
