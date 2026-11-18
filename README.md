# ProcureIQ: Procurement Analytics & Vendor Performance Platform

ProcureIQ is an enterprise data warehouse and business intelligence solution designed to analyze procurement lifecycles, monitor vendor reliability, track spend efficiency, and surface supply chain risks.

## Architecture Overview
The platform implements a Medallion Architecture (Bronze -> Silver -> Gold) with Star Schema dimensional modeling:
- **Bronze Layer**: Raw source data ingestion preserving original event payloads.
- **Silver Layer**: Data cleansing, type casting, referential integrity validation, and anomaly tagging.
- **Gold Layer**: Business marts, vendor scorecards, spend analytics, and compliance monitoring.

## Tech Stack
- **Database / Warehouse**: PostgreSQL & DuckDB
- **Data Engineering**: Python 3.10, Pandas, SQLAlchemy
- **Transformations & Testing**: dbt-compatible SQL models
- **BI & Analytics**: Power BI DAX models, Dimensional Star Schema
