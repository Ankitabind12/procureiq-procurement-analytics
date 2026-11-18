import random
import datetime
from pathlib import Path
import pandas as pd
import numpy as np

from src.config import (
    RAW_DATA_DIR, RANDOM_SEED,
    NUM_VENDORS, NUM_PURCHASE_ORDERS,
    NUM_PO_LINE_ITEMS, NUM_DELIVERIES,
    NUM_INVOICES, NUM_COMPLIANCE_RECORDS
)
from src.utils.logger import logger

def generate_all_datasets():
    """
    Generates realistic, referentially-consistent enterprise procurement datasets:
    - departments.csv
    - categories.csv
    - products.csv
    - date_dimension.csv
    - vendors.csv (500+)
    - vendor_compliance.csv (500+)
    - purchase_orders.csv (5000+)
    - purchase_order_items.csv (8000+)
    - deliveries.csv (5000+)
    - invoices.csv (5000+)
    """
    logger.info("Initializing Realistic Synthetic Procurement Data Generator...")
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    # -------------------------------------------------------------------------
    # 1. DEPARTMENTS MASTER
    # -------------------------------------------------------------------------
    departments_data = [
        {"department_id": "DEP-001", "department_name": "Manufacturing & Operations", "cost_center": "CC-101", "annual_budget": 15000000.0, "manager": "Sarah Jenkins"},
        {"department_id": "DEP-002", "department_name": "Supply Chain & Logistics", "cost_center": "CC-102", "annual_budget": 8500000.0, "manager": "Marcus Vance"},
        {"department_id": "DEP-003", "department_name": "Information Technology", "cost_center": "CC-103", "annual_budget": 12000000.0, "manager": "David Chen"},
        {"department_id": "DEP-004", "department_name": "Research & Development", "cost_center": "CC-104", "annual_budget": 9500000.0, "manager": "Elena Rostova"},
        {"department_id": "DEP-005", "department_name": "Facilities & Maintenance", "cost_center": "CC-105", "annual_budget": 4500000.0, "manager": "Robert Miller"},
        {"department_id": "DEP-006", "department_name": "Quality Assurance", "cost_center": "CC-106", "annual_budget": 3500000.0, "manager": "Patricia Gomez"},
        {"department_id": "DEP-007", "department_name": "Corporate Administration", "cost_center": "CC-107", "annual_budget": 3000000.0, "manager": "Thomas Clark"},
        {"department_id": "DEP-008", "department_name": "Packaging & Assembly", "cost_center": "CC-108", "annual_budget": 6000000.0, "manager": "Aisha Patel"}
    ]
    df_departments = pd.DataFrame(departments_data)
    df_departments.to_csv(RAW_DATA_DIR / "departments.csv", index=False)
    logger.info("Generated departments.csv: %d records", len(df_departments))

    # -------------------------------------------------------------------------
    # 2. CATEGORIES MASTER
    # -------------------------------------------------------------------------
    categories_data = [
        {"category_id": "CAT-001", "category_name": "Raw Industrial Materials", "spend_tier": "Tier 1 - Strategic", "description": "Steel, aluminum alloys, polymers, industrial chemicals"},
        {"category_id": "CAT-002", "category_name": "Industrial Machinery & Tools", "spend_tier": "Tier 1 - Strategic", "description": "CNC tools, hydraulic pumps, replacement parts, robotic components"},
        {"category_id": "CAT-003", "category_name": "Electronic & Electrical", "spend_tier": "Tier 2 - Operational", "description": "Microcontrollers, PCBs, power supplies, sensors, wire harnesses"},
        {"category_id": "CAT-004", "category_name": "Packaging & Freight Supplies", "spend_tier": "Tier 2 - Operational", "description": "Corrugated cartons, pallets, protective wrap, strapping"},
        {"category_id": "CAT-005", "category_name": "IT Hardware & Cloud Infrastructure", "spend_tier": "Tier 1 - Strategic", "description": "Enterprise servers, networking gear, laptops, peripherals"},
        {"category_id": "CAT-006", "category_name": "Facilities & MRO", "spend_tier": "Tier 3 - Tactical", "description": "Safety gear, lubricants, janitorial, HVAC supplies"},
        {"category_id": "CAT-007", "category_name": "Professional & Engineering Services", "spend_tier": "Tier 2 - Operational", "description": "Consulting, engineering audits, specialized fabrication"}
    ]
    df_categories = pd.DataFrame(categories_data)
    df_categories.to_csv(RAW_DATA_DIR / "categories.csv", index=False)
    logger.info("Generated categories.csv: %d records", len(df_categories))

    # -------------------------------------------------------------------------
    # 3. PRODUCTS MASTER (100 SKUs)
    # -------------------------------------------------------------------------
    cat_products_map = {
        "CAT-001": [("Cold Rolled Steel Coil", 450.0, "Metric Ton"), ("Aerospace Grade Aluminum Bar", 620.0, "Metric Ton"), ("High-Density Polyethylene Resin", 180.0, "Metric Ton"), ("Industrial Copper Tubing", 85.0, "Meter"), ("Carbon Fiber Composite Sheet", 320.0, "Square Meter"), ("Nickel Alloy Strip", 540.0, "Kilogram"), ("Titanium Fasteners Pack", 120.0, "Box (100)"), ("Synthetic Lubricant Drum", 210.0, "Barrel (200L)")],
        "CAT-002": [("CNC Carbide End Mill 12mm", 48.5, "Unit"), ("Hydraulic Piston Assembly", 850.0, "Unit"), ("Pneumatic Control Valve 24V", 165.0, "Unit"), ("Heavy Duty Ball Bearing 6205", 28.0, "Unit"), ("Industrial Servo Motor 1.5kW", 1150.0, "Unit"), ("High-Pressure Hose 10m", 72.0, "Unit"), ("Variable Frequency Drive 5HP", 680.0, "Unit"), ("Laser Alignment Sensor", 920.0, "Unit")],
        "CAT-003": [("Microcontroller STM32 Board", 22.5, "Unit"), ("Industrial Power Supply 24V 10A", 95.0, "Unit"), ("Shielded Ethernet Cable Cat6A", 110.0, "Spool (100m)"), ("Relay Module 8-Channel", 34.0, "Unit"), ("Optical Encoder 1000PPR", 145.0, "Unit"), ("High-Voltage Terminal Block", 12.5, "Strip (10)"), ("Circuit Breaker 3-Phase 32A", 58.0, "Unit"), ("Solid State Relay 40A", 42.0, "Unit")],
        "CAT-004": [("Heavy Corrugated Box 24x18x18", 3.2, "Unit"), ("Heat-Treated Euro Pallet", 24.5, "Unit"), ("Industrial Stretch Film 500mm", 18.0, "Roll"), ("Desiccant Silica Gel Packs", 15.0, "Box (500)"), ("Steel Strapping Band 19mm", 65.0, "Roll (300m)"), ("Cushioned Bubble Wrap 100m", 45.0, "Roll"), ("Tamper-Evident Security Seal", 22.0, "Pack (100)"), ("Thermal Shipping Labels 4x6", 28.0, "Roll (1000)")],
        "CAT-005": [("Enterprise Rack Server 1U", 4200.0, "Unit"), ("Managed Network Switch 48-Port", 1850.0, "Unit"), ("Developer Workstation Laptop", 1600.0, "Unit"), ("NVMe Enterprise SSD 3.84TB", 480.0, "Unit"), ("Dual-Band Access Point Wi-Fi 6", 320.0, "Unit"), ("Uninterruptible Power Supply 3kVA", 1250.0, "Unit"), ("Thunderbolt 4 Docking Station", 210.0, "Unit"), ("Ergonomic UltraWide Monitor 34-inch", 550.0, "Unit")],
        "CAT-006": [("ANSI Approved Hard Hat", 25.0, "Unit"), ("Kevlar Cut-Resistant Gloves", 14.5, "Pair"), ("Safety Eyewear Anti-Fog", 8.5, "Unit"), ("Industrial Spill Kit 50 Gallon", 280.0, "Unit"), ("HEPA Air Filter Industrial", 65.0, "Unit"), ("Lithium Complex Grease Cartridge", 9.5, "Tube"), ("Disinfectant Sanitizer Concentrate", 45.0, "Gallon (4x1)"), ("High-Visibility Class 3 Vest", 18.0, "Unit")],
        "CAT-007": [("Precision Metrology Calibration", 1200.0, "Session"), ("ISO Environmental Audit Service", 3500.0, "Audit"), ("Machinery Vibration Diagnostic", 1800.0, "Day"), ("Thermal Imaging Electrical Inspection", 1500.0, "Inspection"), ("Welding Certification Inspection", 950.0, "Batch"), ("Metallurgical Lab Analysis", 750.0, "Sample"), ("Control System PLC Programming", 140.0, "Hour"), ("Cleanroom Environmental Validation", 2800.0, "Audit")]
    }

    products_data = []
    p_counter = 1
    for cat_id, p_list in cat_products_map.items():
        for p_name, u_cost, uom in p_list:
            products_data.append({
                "product_id": f"PRD-{p_counter:04d}",
                "product_name": p_name,
                "category_id": cat_id,
                "standard_cost": round(u_cost, 2),
                "uom": uom,
                "created_date": "2023-01-01"
            })
            p_counter += 1

    # Expand to 100 products
    while len(products_data) < 100:
        base_cat = random.choice(list(cat_products_map.keys()))
        sample_prod = random.choice(cat_products_map[base_cat])
        products_data.append({
            "product_id": f"PRD-{p_counter:04d}",
            "product_name": f"{sample_prod[0]} (Variant #{p_counter})",
            "category_id": base_cat,
            "standard_cost": round(sample_prod[1] * random.uniform(0.85, 1.25), 2),
            "uom": sample_prod[2],
            "created_date": "2023-01-01"
        })
        p_counter += 1

    df_products = pd.DataFrame(products_data)
    df_products.to_csv(RAW_DATA_DIR / "products.csv", index=False)
    logger.info("Generated products.csv: %d records", len(df_products))

    # -------------------------------------------------------------------------
    # 4. DATE DIMENSION (2023-01-01 to 2025-12-31)
    # -------------------------------------------------------------------------
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    date_records = []
    curr = start_date
    while curr <= end_date:
        date_records.append({
            "date_key": int(curr.strftime("%Y%m%d")),
            "full_date": curr.strftime("%Y-%m-%d"),
            "year": curr.year,
            "quarter": f"Q{(curr.month - 1) // 3 + 1}",
            "month": curr.month,
            "month_name": curr.strftime("%B"),
            "day": curr.day,
            "day_of_week": curr.strftime("%A"),
            "is_weekend": curr.weekday() >= 5,
            "fiscal_year": curr.year if curr.month >= 4 else curr.year - 1,
            "fiscal_quarter": f"FQ{((curr.month - 4) % 12) // 3 + 1}"
        })
        curr += datetime.timedelta(days=1)
    df_date_dim = pd.DataFrame(date_records)
    df_date_dim.to_csv(RAW_DATA_DIR / "date_dimension.csv", index=False)
    logger.info("Generated date_dimension.csv: %d records", len(df_date_dim))

    # -------------------------------------------------------------------------
    # 5. VENDORS MASTER (NUM_VENDORS >= 500)
    # -------------------------------------------------------------------------
    vendor_prefixes = [
        "Apex", "Vanguard", "Precision", "Titan", "Pinnacle", "Nexus", "Summit", "Zenith",
        "Alliance", "Global", "Optima", "Sterling", "Quantum", "Omega", "Matrix", "Aegis",
        "Integrity", "Dynamic", "Benchmark", "Pioneer", "Synergy", "Pacific", "Atlas", "Crest"
    ]
    vendor_suffixes = [
        "Industries", "Supply Corp", "Logistics Ltd", "Manufacturing", "Tech Solutions",
        "Materials Group", "International", "Enterprises", "Components", "Engineering",
        "Holdings", "Global Trade", "Systems Inc", "Fabricators", "Products Co"
    ]
    cities = [
        ("Chicago", "USA"), ("Houston", "USA"), ("Detroit", "USA"), ("Frankfurt", "Germany"),
        ("Tokyo", "Japan"), ("Seoul", "South Korea"), ("Toronto", "Canada"), ("Monterrey", "Mexico"),
        ("Birmingham", "UK"), ("Rotterdam", "Netherlands"), ("Singapore", "Singapore"), ("Mumbai", "India")
    ]
    payment_terms_options = ["Net 30", "Net 45", "Net 60", "2/10 Net 30"]

    vendors_data = []
    category_ids = df_categories["category_id"].tolist()
    used_names = set()

    for i in range(1, NUM_VENDORS + 1):
        v_id = f"VND-{i:04d}"
        prefix = random.choice(vendor_prefixes)
        suffix = random.choice(vendor_suffixes)
        name_candidate = f"{prefix} {suffix}"
        if name_candidate in used_names:
            name_candidate = f"{prefix} {suffix} {i}"
        used_names.add(name_candidate)

        city, country = random.choice(cities)
        cat_id = random.choice(category_ids)
        term = random.choice(payment_terms_options)
        
        # Risk profiling: 70% Low, 20% Medium, 10% High
        risk_choice = np.random.choice(["Low", "Medium", "High"], p=[0.70, 0.20, 0.10])
        status = np.random.choice(["Active", "Active", "Active", "Under Review", "Suspended"], p=[0.85, 0.08, 0.03, 0.03, 0.01])
        
        # Quality baseline bias assigned to vendor (some are stellar, some struggle)
        delivery_reliability_bias = float(np.clip(np.random.normal(0.88, 0.10), 0.50, 0.99))
        price_competitiveness_bias = float(np.clip(np.random.normal(1.00, 0.08), 0.80, 1.30))
        quality_defect_rate_bias = float(np.clip(np.random.normal(0.02, 0.015), 0.00, 0.12))

        reg_year = random.choice([2019, 2020, 2021, 2022, 2023])
        reg_month = random.randint(1, 12)
        reg_day = random.randint(1, 28)
        registration_date = f"{reg_year}-{reg_month:02d}-{reg_day:02d}"

        vendors_data.append({
            "vendor_id": v_id,
            "vendor_name": name_candidate,
            "primary_category_id": cat_id,
            "country": country,
            "city": city,
            "contact_email": f"contact@{prefix.lower()}{i}.com",
            "payment_terms": term,
            "risk_rating": risk_choice,
            "vendor_status": status,
            "registration_date": registration_date,
            "delivery_reliability_bias": round(delivery_reliability_bias, 4),
            "price_competitiveness_bias": round(price_competitiveness_bias, 4),
            "quality_defect_rate_bias": round(quality_defect_rate_bias, 4),
            "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
        })

    df_vendors = pd.DataFrame(vendors_data)
    df_vendors.to_csv(RAW_DATA_DIR / "vendors.csv", index=False)
    logger.info("Generated vendors.csv: %d records", len(df_vendors))

    # -------------------------------------------------------------------------
    # 6. VENDOR COMPLIANCE MASTER (NUM_COMPLIANCE_RECORDS >= 500)
    # -------------------------------------------------------------------------
    doc_types = [
        "ISO 9001 (Quality Management)",
        "ISO 14001 (Environmental Management)",
        "ISO 27001 (Information Security)",
        "Commercial General Liability Insurance",
        "Corporate Tax Clearance Certificate",
        "Supplier Code of Conduct & ESG Attestation"
    ]
    compliance_data = []
    
    # Snapshot reference date for current operations
    ref_date = datetime.date(2025, 11, 15)

    for i in range(1, NUM_COMPLIANCE_RECORDS + 1):
        c_id = f"CMP-{i:04d}"
        v_id = f"VND-{((i - 1) % NUM_VENDORS) + 1:04d}"
        d_type = random.choice(doc_types)

        # Issue date between 2023 and 2024
        issue_delta_days = random.randint(300, 750)
        issue_d = ref_date - datetime.timedelta(days=issue_delta_days)
        
        # Expiry scenario: 78% valid active, 14% expired, 8% expiring soon (< 45 days)
        exp_scenario = np.random.choice(["valid", "expired", "expiring_soon"], p=[0.78, 0.14, 0.08])
        if exp_scenario == "valid":
            expiry_d = ref_date + datetime.timedelta(days=random.randint(60, 400))
            status = "Compliant"
            score = random.randint(85, 100)
        elif exp_scenario == "expired":
            expiry_d = ref_date - datetime.timedelta(days=random.randint(5, 180))
            status = "Expired"
            score = random.randint(35, 65)
        else:
            expiry_d = ref_date + datetime.timedelta(days=random.randint(1, 44))
            status = "Pending Renewal"
            score = random.randint(70, 84)

        compliance_data.append({
            "compliance_id": c_id,
            "vendor_id": v_id,
            "document_type": d_type,
            "issue_date": issue_d.strftime("%Y-%m-%d"),
            "expiry_date": expiry_d.strftime("%Y-%m-%d"),
            "compliance_status": status,
            "audit_score": score,
            "auditor_name": random.choice(["Bureau Veritas", "TÜV SÜD", "SGS Global", "Internal Compliance Bureau", "DNV GL"]),
            "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
        })

    df_compliance = pd.DataFrame(compliance_data)
    df_compliance.to_csv(RAW_DATA_DIR / "vendor_compliance.csv", index=False)
    logger.info("Generated vendor_compliance.csv: %d records", len(df_compliance))

    # -------------------------------------------------------------------------
    # 7. PURCHASE ORDERS & LINE ITEMS (5000+ POs, 8000+ Line Items)
    # -------------------------------------------------------------------------
    buyers = ["James Henderson", "Rachel Green", "Carlos Morales", "Hannah Schmidt", "Devin Cooper", "Siddharth Rao"]
    department_ids = df_departments["department_id"].tolist()
    vendor_ids = df_vendors["vendor_id"].tolist()
    product_records = df_products.to_dict(orient="records")
    vendor_lookup = df_vendors.set_index("vendor_id").to_dict(orient="index")

    po_records = []
    po_item_records = []
    item_id_counter = 1

    po_start_date = datetime.date(2023, 1, 15)
    total_days_range = (ref_date - po_start_date).days

    for i in range(1, NUM_PURCHASE_ORDERS + 1):
        po_id = f"PO-{i:06d}"
        v_id = random.choice(vendor_ids)
        dept_id = random.choice(department_ids)
        v_info = vendor_lookup[v_id]

        day_offset = random.randint(0, total_days_range)
        po_date = po_start_date + datetime.timedelta(days=day_offset)
        lead_time = random.randint(7, 35)
        promised_date = po_date + datetime.timedelta(days=lead_time)

        # PO Status distribution: 75% Fulfilled, 12% Partial, 8% Cancelled, 5% Open
        po_status = np.random.choice(["Fulfilled", "Partially Fulfilled", "Cancelled", "Open"], p=[0.75, 0.12, 0.08, 0.05])

        # Generate 1 to 4 line items per PO to guarantee > 8,000 line items
        num_items = np.random.choice([1, 2, 3, 4], p=[0.45, 0.35, 0.15, 0.05])
        po_total = 0.0

        for line_num in range(1, num_items + 1):
            chosen_product = random.choice(product_records)
            p_id = chosen_product["product_id"]
            base_cost = chosen_product["standard_cost"]

            # Quantity ordered based on category
            qty_ordered = int(np.random.choice([10, 25, 50, 100, 250, 500, 1000], p=[0.15, 0.20, 0.25, 0.20, 0.10, 0.07, 0.03]))
            
            # Unit price incorporates vendor competitiveness bias + minor market variance
            unit_price_factor = v_info["price_competitiveness_bias"] * random.uniform(0.96, 1.05)
            # Inject realistic price anomalies occasionally (5% of items)
            if random.random() < 0.05:
                unit_price_factor *= random.choice([1.40, 1.65, 0.60]) # Overpriced or discounted
            unit_price = round(base_cost * unit_price_factor, 2)
            line_total = round(qty_ordered * unit_price, 2)
            po_total += line_total

            po_item_records.append({
                "line_item_id": f"POI-{item_id_counter:07d}",
                "po_id": po_id,
                "line_number": line_num,
                "product_id": p_id,
                "quantity_ordered": qty_ordered,
                "unit_price": unit_price,
                "line_total_amount": line_total,
                "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
            })
            item_id_counter += 1

        po_records.append({
            "po_id": po_id,
            "vendor_id": v_id,
            "department_id": dept_id,
            "order_date": po_date.strftime("%Y-%m-%d"),
            "promised_delivery_date": promised_date.strftime("%Y-%m-%d"),
            "po_status": po_status,
            "currency": "USD",
            "total_po_amount": round(po_total, 2),
            "buyer_name": random.choice(buyers),
            "created_at": po_date.strftime("%Y-%m-%d %H:%M:%S"),
            "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
        })

    df_pos = pd.DataFrame(po_records)
    df_po_items = pd.DataFrame(po_item_records)

    df_pos.to_csv(RAW_DATA_DIR / "purchase_orders.csv", index=False)
    df_po_items.to_csv(RAW_DATA_DIR / "purchase_order_items.csv", index=False)
    logger.info("Generated purchase_orders.csv: %d records", len(df_pos))
    logger.info("Generated purchase_order_items.csv: %d records", len(df_po_items))

    # -------------------------------------------------------------------------
    # 8. DELIVERIES (NUM_DELIVERIES >= 5000)
    # -------------------------------------------------------------------------
    # Match deliveries against non-cancelled POs
    eligible_pos = df_pos[df_pos["po_status"] != "Cancelled"].to_dict(orient="records")
    deliveries_data = []

    for i in range(1, NUM_DELIVERIES + 1):
        del_id = f"DEL-{i:06d}"
        chosen_po = eligible_pos[(i - 1) % len(eligible_pos)]
        po_id = chosen_po["po_id"]
        v_id = chosen_po["vendor_id"]
        v_info = vendor_lookup[v_id]
        promised_d = datetime.date.fromisoformat(chosen_po["promised_delivery_date"])
        po_d = datetime.date.fromisoformat(chosen_po["order_date"])

        # Delivery timing determined by vendor reliability bias
        is_ontime = random.random() < v_info["delivery_reliability_bias"]
        if is_ontime:
            actual_d = promised_d - datetime.timedelta(days=random.randint(0, 4))
            # Ensure delivery is not before PO order date
            if actual_d < po_d:
                actual_d = po_d + datetime.timedelta(days=1)
            del_status = "On-Time"
            delay_days = 0
        else:
            delay_days = int(np.random.exponential(scale=7) + 1)
            actual_d = promised_d + datetime.timedelta(days=delay_days)
            del_status = "Delayed"

        # Quality inspection outcome
        defect_prob = v_info["quality_defect_rate_bias"]
        if random.random() < defect_prob:
            quality_result = "Fail/Rejected" if random.random() < 0.3 else "Minor Defect"
            defect_pct = round(random.uniform(3.5, 18.0), 2)
        else:
            quality_result = "Pass"
            defect_pct = 0.0

        deliveries_data.append({
            "delivery_id": del_id,
            "po_id": po_id,
            "vendor_id": v_id,
            "promised_delivery_date": promised_d.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_d.strftime("%Y-%m-%d"),
            "delay_days": delay_days,
            "delivery_status": del_status,
            "quality_inspection_result": quality_result,
            "defect_rate_percentage": defect_pct,
            "carrier_name": random.choice(["FedEx Freight", "DHL Supply Chain", "Maersk Logistics", "UPS Freight", "Schneider Direct"]),
            "tracking_number": f"TRK-{random.randint(10000000, 99999999)}",
            "received_by": random.choice(["Warehouse Dock A", "Warehouse Dock B", "Central Receiving", "QC Depot 3"]),
            "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
        })

    df_deliveries = pd.DataFrame(deliveries_data)
    df_deliveries.to_csv(RAW_DATA_DIR / "deliveries.csv", index=False)
    logger.info("Generated deliveries.csv: %d records", len(df_deliveries))

    # -------------------------------------------------------------------------
    # 9. INVOICES (NUM_INVOICES >= 5000)
    # -------------------------------------------------------------------------
    # Associate invoices with fulfilled & delivered POs
    invoices_data = []
    
    for i in range(1, NUM_INVOICES + 1):
        inv_id = f"INV-{i:06d}"
        chosen_po = eligible_pos[(i - 1) % len(eligible_pos)]
        po_id = chosen_po["po_id"]
        v_id = chosen_po["vendor_id"]
        base_po_amt = chosen_po["total_po_amount"]
        po_date = datetime.date.fromisoformat(chosen_po["order_date"])

        inv_date = po_date + datetime.timedelta(days=random.randint(7, 30))
        due_date = inv_date + datetime.timedelta(days=random.choice([30, 45, 60]))

        # Invoice Discrepancy Scenarios:
        # 82% Exact Match (Clean 3-way match)
        # 10% Price Discrepancy (Supplier overbilled unit rate by 2% to 15%)
        # 5% Quantity Mismatch (Disputed billing quantity)
        # 3% Significant Outlier / Discrepancy
        discrepancy_type = np.random.choice(
            ["No Discrepancy", "Price Discrepancy", "Quantity Discrepancy", "Severe Variance"],
            p=[0.82, 0.10, 0.05, 0.03]
        )

        if discrepancy_type == "No Discrepancy":
            inv_amount = base_po_amt
            payment_status = np.random.choice(["Paid", "Pending Approval"], p=[0.80, 0.20])
            discrepancy_amount = 0.0
            is_discrepant = False
        elif discrepancy_type == "Price Discrepancy":
            variance_factor = random.uniform(1.03, 1.15)
            inv_amount = round(base_po_amt * variance_factor, 2)
            payment_status = "Disputed"
            discrepancy_amount = round(inv_amount - base_po_amt, 2)
            is_discrepant = True
        elif discrepancy_type == "Quantity Discrepancy":
            variance_factor = random.uniform(1.05, 1.25)
            inv_amount = round(base_po_amt * variance_factor, 2)
            payment_status = "On Hold"
            discrepancy_amount = round(inv_amount - base_po_amt, 2)
            is_discrepant = True
        else: # Severe Variance
            variance_factor = random.uniform(1.20, 1.50)
            inv_amount = round(base_po_amt * variance_factor, 2)
            payment_status = "Disputed"
            discrepancy_amount = round(inv_amount - base_po_amt, 2)
            is_discrepant = True

        invoices_data.append({
            "invoice_id": inv_id,
            "po_id": po_id,
            "vendor_id": v_id,
            "invoice_date": inv_date.strftime("%Y-%m-%d"),
            "payment_due_date": due_date.strftime("%Y-%m-%d"),
            "po_amount": base_po_amt,
            "invoice_amount": inv_amount,
            "discrepancy_amount": discrepancy_amount,
            "is_discrepancy": is_discrepant,
            "discrepancy_reason": discrepancy_type,
            "payment_status": payment_status,
            "currency": "USD",
            "data_source_type": "SYNTHETIC_BUSINESS_SIMULATION"
        })

    df_invoices = pd.DataFrame(invoices_data)
    df_invoices.to_csv(RAW_DATA_DIR / "invoices.csv", index=False)
    logger.info("Generated invoices.csv: %d records", len(df_invoices))

    logger.info("Synthetic Data Generation Completed Successfully!")
    return {
        "departments": len(df_departments),
        "categories": len(df_categories),
        "products": len(df_products),
        "date_dim": len(df_date_dim),
        "vendors": len(df_vendors),
        "compliance": len(df_compliance),
        "purchase_orders": len(df_pos),
        "po_items": len(df_po_items),
        "deliveries": len(df_deliveries),
        "invoices": len(df_invoices)
    }

if __name__ == "__main__":
    generate_all_datasets()
