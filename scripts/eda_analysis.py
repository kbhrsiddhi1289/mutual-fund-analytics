"""
Mutual Fund Analytics Capstone Project
Bluestock Internship
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
nav_df = pd.read_csv("data/raw/02_nav_history.csv")

# Convert date column
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Plot for selected funds
selected_funds = [119551, 120503, 118632]

plt.figure(figsize=(14,7))

for fund in selected_funds:
    sample = nav_df[nav_df['amfi_code'] == fund]

    plt.plot(
        sample['date'],
        sample['nav'],
        label=str(fund)
    )

plt.title("NAV Trend Analysis (2022-2026)")

plt.xlabel("Date")

plt.ylabel("NAV")

plt.legend()
plt.savefig("reports/nav_trend.png")
plt.show()

# AUM Growth Bar Chart

aum_df = pd.read_csv("data/raw/03_aum_by_fund_house.csv")

# Convert date column
aum_df['date'] = pd.to_datetime(aum_df['date'])

# Extract year
aum_df['year'] = aum_df['date'].dt.year

plt.figure(figsize=(14,7))

sns.barplot(
    data=aum_df,
    x='year',
    y='aum_crore',
    hue='fund_house'
)

plt.title("AUM Growth by Fund House (2022-2025)")

plt.xlabel("Year")

plt.ylabel("AUM (Crore)")

plt.xticks(rotation=45)
plt.savefig("reports/aum_growthe.png")
plt.show()

# SIP Inflow Time-Series

sip_df = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")

# Convert month column
sip_df['month'] = pd.to_datetime(sip_df['month'])

plt.figure(figsize=(14,7))

plt.plot(
    sip_df['month'],
    sip_df['sip_inflow_crore'],
    marker='o'
)

plt.title("Monthly SIP Inflow Trend (2022-2025)")

plt.xlabel("Month")

plt.ylabel("SIP Inflow (Crore)")

plt.xticks(rotation=45)
plt.savefig("reports/sip_inflow.png")
plt.show()

# Investor Demographics

investor_df = pd.read_csv("data/raw/08_investor_transactions.csv")



# Age Group Distribution
plt.figure(figsize=(8,8))

investor_df['age_group'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.title("Investor Age Group Distribution")

plt.ylabel("")
plt.savefig("reports/age_distribution.png")
plt.show()


# Gender Split
plt.figure(figsize=(6,6))

sns.countplot(
    data=investor_df,
    x='gender'
)

plt.title("Gender Distribution")
plt.savefig("reports/gender_split.png")
plt.show()

# Geographic Distribution

# SIP Amount by State
state_data = investor_df.groupby('state')['amount_inr'].sum().sort_values(ascending=False)

plt.figure(figsize=(12,7))

state_data.plot(kind='barh')

plt.title("SIP Amount by State")

plt.xlabel("Total SIP Amount")

plt.ylabel("State")
plt.savefig("reports/sip_state.png")
plt.show()


# T30 vs B30 Distribution
plt.figure(figsize=(7,7))

investor_df['city_tier'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.title("T30 vs B30 City Tier Distribution")

plt.ylabel("")
plt.savefig("reports/t30_vs_b30.png")
plt.show()

# NAV Return Correlation Heatmap

nav_df = pd.read_csv("data/raw/02_nav_history.csv")

# Convert date
nav_df['date'] = pd.to_datetime(nav_df['date'])

# Pivot table
pivot_df = nav_df.pivot(
    index='date',
    columns='amfi_code',
    values='nav'
)

# Daily returns
returns_df = pivot_df.pct_change()

# Correlation
corr_matrix = returns_df.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    corr_matrix,
    annot=False,
    cmap='coolwarm'
)

plt.title("NAV Return Correlation Matrix")
plt.savefig("reports/nav_return.png")
plt.show()

# Sector Allocation Donut Chart

portfolio_df = pd.read_csv("data/raw/09_portfolio_holdings.csv")



# Aggregate sector weights
sector_data = portfolio_df.groupby('sector')['weight_pct'].sum()

plt.figure(figsize=(8,8))

plt.pie(
    sector_data,
    labels=sector_data.index,
    autopct='%1.1f%%'
)

# Create donut effect
centre_circle = plt.Circle((0,0), 0.70, fc='white')

fig = plt.gcf()

fig.gca().add_artist(centre_circle)

plt.title("Sector Allocation Across Equity Funds")
plt.savefig("reports/sector_allocation.png")
plt.show()

# Category Inflow Heatmap

category_df = pd.read_csv("data/raw/05_category_inflows.csv")



# Pivot for heatmap
heatmap_data = category_df.pivot(
    index='category',
    columns='month',
    values='net_inflow_crore'
)

plt.figure(figsize=(14,8))

sns.heatmap(
    heatmap_data,
    cmap='YlGnBu'
)

plt.title("Category-wise Net Inflow Heatmap")
plt.savefig("reports/category_inflow.png")
plt.show()