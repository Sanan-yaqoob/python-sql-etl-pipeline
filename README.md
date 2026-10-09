# Python-SQL ETL Pipeline

## Overview

An end-to-end ETL pipeline using Python, Pandas, SQLAlchemy and SQLite.

The project extracts retail order data from CSV, cleans and transforms the data, performs data-quality checks, loads it into a SQLite database, and performs SQL-based business analysis.

## Technologies

- Python
- Pandas
- SQLAlchemy
- SQLite
- Matplotlib
- Jupyter Notebook

## Workflow

CSV → Extract → Transform → Validate → SQLite → SQL Analysis

## How to Run

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline:

```bash
python src/pipeline.py
```

Run the SQL analysis:

```bash
python src/sql_analysis.py
```

The Jupyter notebook `notebooks/etl_analysis.ipynb` can be used to explore the data and visualise the results.

## Key Analysis

- Monthly revenue and profit
- Product performance
- Regional performance
- Units sold
- Profit margins