from pathlib import Path
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "warehouse" / "sales.db"
engine = create_engine(f"sqlite:///{DB}")

queries = {
    "Monthly revenue and profit": """
        SELECT order_month, ROUND(SUM(revenue), 2) AS revenue,
               ROUND(SUM(profit), 2) AS profit
        FROM sales GROUP BY order_month ORDER BY order_month
    """,
    "Top products": """
        SELECT product, SUM(quantity) AS units_sold,
               ROUND(SUM(revenue), 2) AS revenue,
               ROUND(SUM(profit), 2) AS profit
        FROM sales GROUP BY product ORDER BY revenue DESC
    """,
    "Regional performance": """
        SELECT region, ROUND(SUM(revenue), 2) AS revenue,
               ROUND(SUM(profit), 2) AS profit
        FROM sales GROUP BY region ORDER BY revenue DESC
    """
}
with engine.connect() as conn:
    for title, sql in queries.items():
        print(f"\n## {title}")
        for row in conn.execute(text(sql)):
            print(row)
