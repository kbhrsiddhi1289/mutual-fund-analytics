from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///bluestock_mf.db')

df = pd.read_csv("data/processed/nav_history_cleaned.csv")

df.to_sql("fact_nav", engine, if_exists='replace', index=False)

print("Data loaded into SQLite")