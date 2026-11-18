import json
from pathlib import Path
import duckdb
import pandas as pd

from src.config import DUCKDB_PATH, BASE_DIR
from src.utils.logger import logger

class KPIEngine:
    """
    KPI Engine & Business Analytics Service:
    Calculates the 10 core executive procurement KPIs and generates empirical
    business recommendations derived strictly from warehouse data.
    """

    def __init__(self, db_path: Path = DUCKDB_PATH):
        self.db_path = db_path

    def get_connection(self):
        return duckdb.connect(str(self.db_path))

    def compute_kpis(self) -> dict:
        logger.info("Computing Core Procurement KPIs from Gold/Silver Data Marts...")
        con = self.get_connection()

        # 1. Total Spend, Total POs, PO Fulfilment Rate, PO Cancellation Rate, Avg PO Cost
        po_query = """
        SELECT 
            COUNT(po_id) AS total_pos,
            ROUND(SUM(total_po_amount), 2) AS total_procurement_spend,
            ROUND(AVG(total_po_amount), 2) AS avg_po_cost,
            ROUND(CAST(SUM(is_fulfilled) AS NUMERIC) / NULLIF(COUNT(po_id), 0) * 100.0, 2) AS po_fulfilment_rate,
            ROUND(CAST(SUM(is_cancelled) AS NUMERIC) / NULLIF(COUNT(po_id), 0) * 100.0, 2) AS po_cancellation_rate
        FROM silver_purchase_orders;
        """
        po_metrics = con.execute(po_query).fetchdf().to_dict(orient="records")[0]

        # Average Line Unit Price
        avg_unit_cost = con.execute("SELECT ROUND(AVG(unit_price), 2) FROM silver_purchase_order_items;").fetchone()[0]
        po_metrics["avg_unit_purchase_price"] = avg_unit_cost

        # 2. On-Time Delivery Rate & Average Delivery Delay
        del_query = """
        SELECT 
            COUNT(delivery_id) AS total_deliveries,
            ROUND(CAST(SUM(is_ontime) AS NUMERIC) / NULLIF(COUNT(delivery_id), 0) * 100.0, 2) AS ontime_delivery_rate,
            ROUND(AVG(delay_days), 2) AS avg_delivery_delay_days,
            ROUND(CAST(SUM(is_quality_pass) AS NUMERIC) / NULLIF(COUNT(delivery_id), 0) * 100.0, 2) AS quality_pass_rate
        FROM silver_deliveries;
        """
        del_metrics = con.execute(del_query).fetchdf().to_dict(orient="records")[0]

        # 3. Invoice Discrepancy Rate & Total Leakage
        inv_query = """
        SELECT 
            COUNT(invoice_id) AS total_invoices,
            ROUND(CAST(SUM(CASE WHEN is_discrepancy = true THEN 1 ELSE 0 END) AS NUMERIC) / NULLIF(COUNT(invoice_id), 0) * 100.0, 2) AS invoice_discrepancy_rate,
            ROUND(SUM(discrepancy_amount), 2) AS total_invoice_discrepancy_leakage,
            ROUND(SUM(invoice_amount), 2) AS total_invoiced_spend
        FROM silver_invoices;
        """
        inv_metrics = con.execute(inv_query).fetchdf().to_dict(orient="records")[0]

        # 4. Vendor Compliance Rate
        comp_query = """
        SELECT 
            COUNT(compliance_id) AS total_compliance_audits,
            ROUND(CAST(SUM(CASE WHEN compliance_status = 'Compliant' THEN 1 ELSE 0 END) AS NUMERIC) / NULLIF(COUNT(compliance_id), 0) * 100.0, 2) AS vendor_compliance_rate,
            SUM(CASE WHEN compliance_risk_tier = 'HIGH RISK - EXPIRED' THEN 1 ELSE 0 END) AS expired_documents_count,
            ROUND(AVG(audit_score), 2) AS avg_audit_score
        FROM silver_vendor_compliance;
        """
        comp_metrics = con.execute(comp_query).fetchdf().to_dict(orient="records")[0]

        # 5. Department-wise Spend
        dept_spend_query = """
        SELECT 
            dept.department_name,
            ROUND(SUM(po.total_po_amount), 2) AS department_spend,
            ROUND(SUM(po.total_po_amount) / (SELECT SUM(total_po_amount) FROM silver_purchase_orders) * 100.0, 2) AS spend_share_pct
        FROM silver_purchase_orders po
        JOIN silver_departments dept ON po.department_id = dept.department_id
        GROUP BY dept.department_name
        ORDER BY department_spend DESC;
        """
        dept_spend = con.execute(dept_spend_query).fetchdf().to_dict(orient="records")

        # 6. Overall Vendor Scorecard Summary
        scorecard_query = """
        SELECT 
            ROUND(AVG(composite_performance_score), 2) AS avg_vendor_performance_score,
            ROUND(AVG(delivery_reliability_score), 2) AS avg_reliability_score,
            ROUND(AVG(price_competitiveness_score), 2) AS avg_price_score,
            ROUND(AVG(product_quality_score), 2) AS avg_quality_score,
            ROUND(AVG(compliance_score), 2) AS avg_compliance_pillar_score,
            SUM(CASE WHEN vendor_performance_tier = 'Tier 1 - Strategic Partner' THEN 1 ELSE 0 END) AS tier1_partners_count,
            SUM(CASE WHEN vendor_performance_tier = 'Tier 2 - Preferred Supplier' THEN 1 ELSE 0 END) AS tier2_preferred_count,
            SUM(CASE WHEN vendor_performance_tier = 'Tier 3 - Operational Supplier' THEN 1 ELSE 0 END) AS tier3_operational_count,
            SUM(CASE WHEN vendor_performance_tier = 'Tier 4 - High Risk / PIP Required' THEN 1 ELSE 0 END) AS tier4_high_risk_count
        FROM gold_vendor_scorecard;
        """
        scorecard_metrics = con.execute(scorecard_query).fetchdf().to_dict(orient="records")[0]

        # Top 5 Best Performing Vendors
        top_vendors = con.execute("""
            SELECT vendor_id, vendor_name, primary_category, composite_performance_score, vendor_performance_tier, total_spend
            FROM gold_vendor_scorecard
            ORDER BY composite_performance_score DESC, total_spend DESC
            LIMIT 5;
        """).fetchdf().to_dict(orient="records")

        # Bottom 5 Vendors Needing PIP
        bottom_vendors = con.execute("""
            SELECT vendor_id, vendor_name, primary_category, composite_performance_score, vendor_performance_tier, ontime_delivery_rate, avg_delay_days, total_spend
            FROM gold_vendor_scorecard
            WHERE total_orders > 0
            ORDER BY composite_performance_score ASC
            LIMIT 5;
        """).fetchdf().to_dict(orient="records")

        # Top 3 High Spend Categories
        top_categories = con.execute("""
            SELECT category_name, spend_tier, total_category_spend, active_suppliers_count
            FROM gold_category_performance
            ORDER BY total_category_spend DESC
            LIMIT 3;
        """).fetchdf().to_dict(orient="records")

        con.close()

        kpi_report = {
            "summary_kpis": {
                "1_total_procurement_spend": po_metrics["total_procurement_spend"],
                "2_vendor_ontime_delivery_rate_pct": del_metrics["ontime_delivery_rate"],
                "3_avg_delivery_delay_days": del_metrics["avg_delivery_delay_days"],
                "4_po_fulfilment_rate_pct": po_metrics["po_fulfilment_rate"],
                "5_invoice_discrepancy_rate_pct": inv_metrics["invoice_discrepancy_rate"],
                "6_vendor_compliance_rate_pct": comp_metrics["vendor_compliance_rate"],
                "7_avg_purchase_cost_po": po_metrics["avg_po_cost"],
                "7b_avg_purchase_price_sku": po_metrics["avg_unit_purchase_price"],
                "8_department_spend_breakdown": dept_spend,
                "9_avg_vendor_performance_score": scorecard_metrics["avg_vendor_performance_score"],
                "10_po_cancellation_rate_pct": po_metrics["po_cancellation_rate"]
            },
            "scorecard_distribution": scorecard_metrics,
            "top_performing_vendors": top_vendors,
            "vendors_requiring_improvement": bottom_vendors,
            "highest_spend_categories": top_categories,
            "leakage_exposure": {
                "total_leakage_dollars": inv_metrics["total_invoice_discrepancy_leakage"],
                "expired_certs_count": comp_metrics["expired_documents_count"]
            }
        }

        # Write KPI output to JSON artifact
        output_path = BASE_DIR / "docs" / "kpi_summary_results.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(kpi_report, f, indent=2)
        logger.info("Saved KPI Summary Results to %s", output_path)

        return kpi_report

if __name__ == "__main__":
    engine = KPIEngine()
    engine.compute_kpis()
