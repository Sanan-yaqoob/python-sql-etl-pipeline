from pathlib import Path
import logging
import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "orders.csv"
DB_DIR = ROOT / "data" / "warehouse"
DB_PATH = DB_DIR / "sales.db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def extract(path=INPUT):
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path)
    log.info("Extracted %s rows", len(df))
    return df

def transform(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    required = {"order_id", "order_date", "customer_id", "product", "category",
                "quantity", "unit_price", "unit_cost", "region"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.drop_duplicates(subset=["order_id"])
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "unit_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["order_id", "order_date", "product", "quantity",
                           "unit_price", "unit_cost"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0) & (df["unit_cost"] >= 0)]
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["cost"] = (df["quantity"] * df["unit_cost"]).round(2)
    df["profit"] = (df["revenue"] - df["cost"]).round(2)
    df["profit_margin"] = (df["profit"] / df["revenue"].replace(0, float("nan"))).round(4)
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df

def validate(df):
    if not df["order_id"].is_unique:
        raise ValueError("order_id values must be unique")
    if not df["quantity"].gt(0).all():
        raise ValueError("Quantity must be positive")
    if not df["profit"].notna().all():
        raise ValueError("Profit contains null values")
    log.info("Data-quality checks passed")

def load(df):
    DB_DIR.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.begin() as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)"))
    log.info("Loaded %s rows into %s", len(df), DB_PATH)

def main():
    transformed = transform(extract())
    validate(transformed)
    load(transformed)
    log.info("ETL completed successfully")

if __name__ == "__main__":
    main()
