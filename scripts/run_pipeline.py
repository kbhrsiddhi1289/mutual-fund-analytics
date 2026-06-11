import os

os.system("python scripts/data_cleaning.py")
os.system("python scripts/load_to_sqlite.py")
os.system("python scripts/eda_analysis.py")
os.system("python scripts/performance_analytics.py")
os.system("python scripts/advanced_analytics.py")

print("Pipeline Completed Successfully")