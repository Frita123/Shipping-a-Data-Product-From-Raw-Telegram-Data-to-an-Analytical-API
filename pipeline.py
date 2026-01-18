# pipeline.py
from dagster import job, op
import subprocess
import os

# ---------------------------
# Config: Paths to scripts
# ---------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
DBT_DIR = os.path.join(PROJECT_ROOT, "medical_warehouse")

# ---------------------------
# Ops
# ---------------------------

@op
def scrape_telegram_data():
    """Scrape Telegram data."""
    print("Starting Telegram scraping...")
    subprocess.run(["python", os.path.join(SRC_DIR, "scrape_telegram.py")], check=True)
    print("Telegram scraping complete.")
    return "scrape_done"

@op
def load_raw_to_postgres(scrape_done):
    """Load raw JSON data into PostgreSQL."""
    print("Loading raw data to PostgreSQL...")
    subprocess.run(["python", os.path.join(SRC_DIR, "load_raw_to_postgres.py")], check=True)
    print("Raw data loaded successfully.")
    return "load_done"

@op
def run_dbt_transformations(load_done):
    """Run dbt models to build data warehouse tables."""
    print("Running dbt transformations...")
    subprocess.run(["dbt", "run"], cwd=DBT_DIR, check=True)
    print("dbt models executed successfully.")
    return "dbt_done"

@op
def run_yolo_enrichment(dbt_done):
    """Run YOLO object detection enrichment."""
    print("Running YOLO object detection...")
    subprocess.run(["python", os.path.join(SRC_DIR, "yolo_detect.py")], check=True)
    print("YOLO enrichment complete.")
    return "yolo_done"

# ---------------------------
# Job Graph
# ---------------------------

@job
def telegram_pipeline():
    """
    Full pipeline:
    scrape -> load raw -> dbt -> YOLO enrichment
    """
    # Outputs of one op are passed as inputs to the next to set dependency
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)
