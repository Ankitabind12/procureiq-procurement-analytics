# ProcureIQ: Installation & Setup Guide

This guide walks you through setting up and running the ProcureIQ platform on your local machine or server.

---

### 1. System Prerequisites
- **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+)
- **Python**: Version `3.9` to `3.12` (`python --version`)
- **Git**: Installed and configured (`git --version`)
- **Database (Choose Option A or B)**:
  - **Option A (Default - Zero Setup)**: Embedded **DuckDB** (Installed via pip; zero external services required).
  - **Option B (Enterprise)**: **PostgreSQL 13+** (Local or cloud RDS/Supabase).

---

### 2. Clone the Repository
```bash
git clone https://github.com/Ankitabind12/procureiq-procurement-analytics.git
cd procureiq-procurement-analytics
```

---

### 3. Create & Activate Virtual Environment
#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Core libraries installed:
- `pandas`, `numpy`: Vectorized data transformation and aggregations
- `duckdb`: High-performance embedded OLAP columnar database
- `sqlalchemy`, `psycopg-binary`: PostgreSQL connection drivers
- `scikit-learn`: Statistical anomaly and price outlier detection
- `pytest`: Automated data integrity and pipeline testing suite

---

### 5. Configure Environment Variables
Copy the provided template:
```bash
cp .env.example .env
```

#### For Default Zero-Setup Mode (Recommended):
No modifications needed! ProcureIQ defaults to high-speed DuckDB embedded data warehousing.

#### For PostgreSQL Mode (Optional):
Edit `.env` with your PostgreSQL database credentials:
```env
DB_ENGINE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=procureiq_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
```

Create the database in PostgreSQL before executing:
```sql
CREATE DATABASE procureiq_dw;
```

---

### 6. Verify Installation
Run the automated test suite:
```bash
pytest
```
All tests should pass. You are now ready to run the pipeline!
