import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Storage Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GOLD_EXPORTS_DIR = DATA_DIR / "gold_exports"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
GOLD_EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
DB_ENGINE_TYPE = os.getenv("DB_ENGINE", "duckdb").lower()  # 'postgresql' or 'duckdb'

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "procureiq_dw")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

POSTGRES_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DUCKDB_PATH = BASE_DIR / "procureiq_dw.duckdb"

# Data Generation Volumes (Meets or exceeds all enterprise scale specs)
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
NUM_VENDORS = int(os.getenv("NUM_VENDORS", "500"))
NUM_PURCHASE_ORDERS = int(os.getenv("NUM_PURCHASE_ORDERS", "5000"))
NUM_PO_LINE_ITEMS = int(os.getenv("NUM_PO_LINE_ITEMS", "8000"))
NUM_DELIVERIES = int(os.getenv("NUM_DELIVERIES", "5000"))
NUM_INVOICES = int(os.getenv("NUM_INVOICES", "5000"))
NUM_COMPLIANCE_RECORDS = int(os.getenv("NUM_COMPLIANCE_RECORDS", "500"))
