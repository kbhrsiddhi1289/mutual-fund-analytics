# Data Dictionary

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| amfi_code | INTEGER | Unique mutual fund identifier |
| scheme_name | TEXT | Name of mutual fund scheme |
| fund_house | TEXT | Mutual fund company name |
| category | TEXT | Fund category |
| nav | REAL | Net Asset Value |
| date | DATE | NAV date |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Transaction amount in INR |
| expense_ratio_pct | REAL | Expense ratio percentage |
| return_1yr_pct | REAL | 1 year return percentage |
| return_3yr_pct | REAL | 3 year return percentage |
| return_5yr_pct | REAL | 5 year return percentage |
| kyc_status | TEXT | Investor KYC verification status |
| state | TEXT | Investor state |
| city | TEXT | Investor city |

## Source References

- 02_nav_history.csv
- 07_scheme_performance.csv
- 08_investor_transactions.csv
- 01_fund_master.csv