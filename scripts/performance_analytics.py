"""
Mutual Fund Analytics Capstone Project
Bluestock Internship
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load NAV dataset
nav_df = pd.read_csv("data/raw/02_nav_history.csv")

# Convert date
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Sort values
nav_df = nav_df.sort_values(['amfi_code', 'date'])




# Daily Returns
nav_df['daily_return'] = nav_df.groupby('amfi_code')['nav'].pct_change()

print(nav_df[['amfi_code', 'date', 'daily_return']].head())

print("\nDaily Return Summary:")

print(nav_df['daily_return'].describe())

# CAGR Calculation

cagr_list = []

for fund in nav_df['amfi_code'].unique():

    fund_data = nav_df[nav_df['amfi_code'] == fund]

    start_nav = fund_data.iloc[0]['nav']

    end_nav = fund_data.iloc[-1]['nav']

    years = 4   # Approx 2022–2026

    cagr = ((end_nav / start_nav) ** (1 / years)) - 1

    cagr_list.append({
        'amfi_code': fund,
        'start_nav': start_nav,
        'end_nav': end_nav,
        'cagr': cagr
    })

cagr_df = pd.DataFrame(cagr_list)

print("\nCAGR Table:")

print(cagr_df.head())

# Sharpe Ratio

risk_free_rate = 0.065

sharpe_list = []

for fund in nav_df['amfi_code'].unique():

    fund_data = nav_df[nav_df['amfi_code'] == fund]

    mean_return = fund_data['daily_return'].mean() * 252

    std_return = fund_data['daily_return'].std() * np.sqrt(252)

    sharpe_ratio = (mean_return - risk_free_rate) / std_return

    sharpe_list.append({
        'amfi_code': fund,
        'sharpe_ratio': sharpe_ratio
    })

sharpe_df = pd.DataFrame(sharpe_list)

# Rank funds
sharpe_df = sharpe_df.sort_values(
    by='sharpe_ratio',
    ascending=False
)

print("\nSharpe Ratio Ranking:")

print(sharpe_df.head())

# Sortino Ratio

sortino_list = []

for fund in nav_df['amfi_code'].unique():

    fund_data = nav_df[nav_df['amfi_code'] == fund]

    mean_return = fund_data['daily_return'].mean() * 252

    # Downside returns only
    downside_returns = fund_data[
        fund_data['daily_return'] < 0
    ]['daily_return']

    downside_std = downside_returns.std() * np.sqrt(252)

    sortino_ratio = (mean_return - risk_free_rate) / downside_std

    sortino_list.append({
        'amfi_code': fund,
        'sortino_ratio': sortino_ratio
    })

sortino_df = pd.DataFrame(sortino_list)

sortino_df = sortino_df.sort_values(
    by='sortino_ratio',
    ascending=False
)

print("\nSortino Ratio Ranking:")

print(sortino_df.head())

# Maximum Drawdown

drawdown_list = []

for fund in nav_df['amfi_code'].unique():

    fund_data = nav_df[
        nav_df['amfi_code'] == fund
    ].copy()

    # Running max NAV
    fund_data['running_max'] = fund_data['nav'].cummax()

    # Drawdown
    fund_data['drawdown'] = (
        fund_data['nav'] /
        fund_data['running_max']
    ) - 1

    max_drawdown = fund_data['drawdown'].min()

    drawdown_list.append({
        'amfi_code': fund,
        'max_drawdown': max_drawdown
    })

drawdown_df = pd.DataFrame(drawdown_list)

drawdown_df = drawdown_df.sort_values(
    by='max_drawdown'
)

print("\nMaximum Drawdown Ranking:")

print(drawdown_df.head())

# Fund Scorecard

# Merge all metrics
scorecard_df = cagr_df.merge(
    sharpe_df,
    on='amfi_code'
)

scorecard_df = scorecard_df.merge(
    sortino_df,
    on='amfi_code'
)

scorecard_df = scorecard_df.merge(
    drawdown_df,
    on='amfi_code'
)

# Ranking scores
scorecard_df['return_rank'] = scorecard_df['cagr'].rank(ascending=False)

scorecard_df['sharpe_rank'] = scorecard_df['sharpe_ratio'].rank(ascending=False)

scorecard_df['sortino_rank'] = scorecard_df['sortino_ratio'].rank(ascending=False)

scorecard_df['drawdown_rank'] = scorecard_df['max_drawdown'].rank(ascending=True)

# Composite Score
scorecard_df['fund_score'] = (
    scorecard_df['return_rank'] * 0.4 +
    scorecard_df['sharpe_rank'] * 0.3 +
    scorecard_df['sortino_rank'] * 0.2 +
    scorecard_df['drawdown_rank'] * 0.1
)

# Sort by best score
scorecard_df = scorecard_df.sort_values(
    by='fund_score'
)

print("\nFund Scorecard:")

print(scorecard_df.head())

# Save CSV
scorecard_df.to_csv(
    "reports/fund_scorecard.csv",
    index=False
)

# Alpha and Beta

benchmark_df = nav_df.groupby('date')['daily_return'].mean().reset_index()

benchmark_df.rename(
    columns={'daily_return': 'benchmark_return'},
    inplace=True
)

alpha_beta_list = []

for fund in nav_df['amfi_code'].unique():

    fund_data = nav_df[
        nav_df['amfi_code'] == fund
    ][['date', 'daily_return']]

    merged = pd.merge(
        fund_data,
        benchmark_df,
        on='date'
    ).dropna()

    slope, intercept, r_value, p_value, std_err = linregress(
        merged['benchmark_return'],
        merged['daily_return']
    )

    beta = slope

    alpha = intercept * 252

    alpha_beta_list.append({
        'amfi_code': fund,
        'alpha': alpha,
        'beta': beta
    })

alpha_beta_df = pd.DataFrame(alpha_beta_list)

print("\nAlpha Beta Table:")

print(alpha_beta_df.head())

# Save CSV
alpha_beta_df.to_csv(
    "reports/alpha_beta.csv",
    index=False
)

# Benchmark Comparison Chart

top_funds = scorecard_df.head(5)['amfi_code']

plt.figure(figsize=(12,6))

for fund in top_funds:

    fund_data = nav_df[
        nav_df['amfi_code'] == fund
    ]

    plt.plot(
        fund_data['date'],
        fund_data['nav'],
        label=str(fund)
    )

plt.title("Top 5 Funds NAV Comparison")

plt.xlabel("Date")

plt.ylabel("NAV")

plt.legend()

plt.savefig("reports/benchmark_comparison.png")

plt.show()