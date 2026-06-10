import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
nav_df = pd.read_csv("data/processed/nav_history_cleaned.csv")
txn_df = pd.read_csv("data/processed/investor_transactions_cleaned.csv")
perf_df = pd.read_csv("data/processed/scheme_performance_cleaned.csv")
portfolio_df = pd.read_csv("data/raw/09_portfolio_holdings.csv")
nav_df['date'] = pd.to_datetime(nav_df['date'])

nav_df = nav_df.sort_values(['amfi_code', 'date'])

nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()
risk_metrics = []

for code in nav_df['amfi_code'].unique():

    temp = nav_df[nav_df['amfi_code'] == code]

    returns = temp['daily_return'].dropna()

    var_95 = np.percentile(returns, 5)

    cvar_95 = returns[returns <= var_95].mean()

    risk_metrics.append([code, var_95, cvar_95])

risk_df = pd.DataFrame(
    risk_metrics,
    columns=['amfi_code', 'VaR_95', 'CVaR_95']
)

print(risk_df.head())

risk_df.to_csv(
    "reports/var_cvar_report.csv",
    index=False
)
key_funds = nav_df['amfi_code'].unique()[:5]

plt.figure(figsize=(12,6))

for code in key_funds:

    temp = nav_df[nav_df['amfi_code'] == code]

    rolling_sharpe = (
        temp['daily_return'].rolling(90).mean()
        /
        temp['daily_return'].rolling(90).std()
    ) * np.sqrt(252)

    plt.plot(
        temp['date'],
        rolling_sharpe,
        label=str(code)
    )

plt.legend()

plt.title("Rolling 90-Day Sharpe Ratio")

plt.savefig(
    "reports/rolling_sharpe_chart.png"
)

plt.show()
txn_df['transaction_date'] = pd.to_datetime(
    txn_df['transaction_date']
)

txn_df['cohort_year'] = txn_df['transaction_date'].dt.year

cohort = txn_df.groupby('cohort_year').agg({
    'amount_inr': ['mean', 'sum']
})

print("\nCohort Analysis:")
print(cohort)

txn_df['month'] = txn_df['transaction_date'].dt.to_period('M')

sip_counts = txn_df.groupby(
    ['investor_id', 'month']
).size().reset_index(name='txn_count')

sip_continuity = sip_counts.groupby(
    'investor_id'
)['month'].nunique()

print("\nSIP Continuity:")
print(sip_continuity.head())
from sklearn.metrics.pairwise import cosine_similarity

pivot = nav_df.pivot_table(
    index='date',
    columns='amfi_code',
    values='daily_return'
).fillna(0)

similarity = cosine_similarity(
    pivot.T
)

similarity_df = pd.DataFrame(
    similarity,
    index=pivot.columns,
    columns=pivot.columns
)

print("\nFund Similarity Matrix:")
print(similarity_df.iloc[:5, :5])
fund_df = pd.read_csv(
    "data/raw/03_aum_by_fund_house.csv"
)

print(fund_df.columns)

aum_total = fund_df['aum_crore'].sum()

fund_df['market_share'] = (
    fund_df['aum_crore'] / aum_total
)

hhi = (
    (fund_df['market_share'] * 100) ** 2
).sum()

print("\nHHI Concentration Index:")
print(hhi)