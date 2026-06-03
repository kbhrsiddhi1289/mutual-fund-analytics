import pandas as pd

# -------------------------------
# CLEAN NAV HISTORY
# -------------------------------

nav_df = pd.read_csv(
    "data/raw/02_nav_history.csv",
    on_bad_lines='skip'
)

print(nav_df.columns)
# Convert date column
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Sort values
nav_df = nav_df.sort_values(['amfi_code', 'date'])

# Remove duplicates
nav_df = nav_df.drop_duplicates()

# Forward fill missing NAV values
nav_df['nav'] = nav_df['nav'].ffill()

# Keep only valid NAV values
nav_df = nav_df[nav_df['nav'] > 0]

# Save cleaned file
nav_df.to_csv(
    "data/processed/nav_history_cleaned.csv",
    index=False
)

print("nav_history cleaned successfully")


# -------------------------------
# CLEAN INVESTOR TRANSACTIONS
# -------------------------------

txn_df = pd.read_csv(
    "data/raw/08_investor_transactions.csv",
    on_bad_lines='skip'
)
print(txn_df.columns)
# Standardize transaction types
txn_df['transaction_type'] = (
    txn_df['transaction_type']
    .str.upper()
)

# Keep valid transaction types
valid_types = ['SIP', 'LUMPSUM', 'REDEMPTION']

txn_df = txn_df[
    txn_df['transaction_type'].isin(valid_types)
]

# Keep amount > 0
txn_df = txn_df[txn_df['amount_inr'] > 0]
# Convert date format
txn_df['transaction_date'] = pd.to_datetime(
    txn_df['transaction_date']
)

# Check KYC values
print("\nKYC Status Values:")
print(txn_df['kyc_status'].unique())

# Save cleaned file
txn_df.to_csv(
    "data/processed/investor_transactions_cleaned.csv",
    index=False
)

print("investor_transactions cleaned successfully")


# -------------------------------
# CLEAN SCHEME PERFORMANCE
# -------------------------------

perf_df = pd.read_csv(
    "data/raw/07_scheme_performance.csv",
    on_bad_lines='skip'
)
perf_df = pd.read_csv(
    "data/raw/07_scheme_performance.csv",
    on_bad_lines='skip'
)

print(perf_df.columns)
# Convert return columns to numeric
return_columns = [
    'return_1yr_pct',
    'return_3yr_pct',
    'return_5yr_pct'
]

for col in return_columns:
    perf_df[col] = pd.to_numeric(
        perf_df[col],
        errors='coerce'
    )

# Convert expense ratio
perf_df['expense_ratio'] = pd.to_numeric(
    perf_df['expense_ratio_pct'],
    errors='coerce'
)

# Find anomalies
anomalies = perf_df[
    (perf_df['expense_ratio_pct'] < 0.1) |
    (perf_df['expense_ratio_pct'] > 2.5)
]

print("\nExpense Ratio Anomalies:")
print(anomalies)

# Save cleaned file
perf_df.to_csv(
    "data/processed/scheme_performance_cleaned.csv",
    index=False
)

print("scheme_performance cleaned successfully")


# -------------------------------
# DATA QUALITY SUMMARY
# -------------------------------

print("\nData Cleaning Completed Successfully")
print("Processed files saved in data/processed/")