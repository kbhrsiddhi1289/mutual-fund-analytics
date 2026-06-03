from sqlalchemy import create_engine
import pandas as pd

# Create SQLite database
engine = create_engine('sqlite:///bluestock_mf.db')

# Load cleaned CSV files
nav_df = pd.read_csv("data/processed/nav_history_cleaned.csv")

txn_df = pd.read_csv(
    "data/processed/investor_transactions_cleaned.csv"
)

perf_df = pd.read_csv(
    "data/processed/scheme_performance_cleaned.csv"
)

# Save to SQLite tables
nav_df.to_sql(
    "fact_nav",
    engine,
    if_exists='replace',
    index=False
)

txn_df.to_sql(
    "fact_transactions",
    engine,
    if_exists='replace',
    index=False
)

perf_df.to_sql(
    "fact_performance",
    engine,
    if_exists='replace',
    index=False
)

print("All cleaned datasets loaded into SQLite successfully")