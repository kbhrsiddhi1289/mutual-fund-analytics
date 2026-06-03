-- 1. Top 5 funds by AUM
SELECT scheme_name, aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV
SELECT AVG(nav) AS average_nav
FROM fact_nav;

-- 3. Monthly average NAV
SELECT substr(date, 1, 7) AS month,
AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY month;

-- 4. Transactions by state
SELECT state, COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- 5. Funds with expense ratio < 1%
SELECT amfi_code, expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1;

-- 6. Highest 1 year return
SELECT amfi_code, return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 5;

-- 7. Count of SIP transactions
SELECT COUNT(*) AS sip_count
FROM fact_transactions
WHERE transaction_type = 'SIP';

-- 8. Average transaction amount
SELECT AVG(amount_inr) AS avg_transaction
FROM fact_transactions;

-- 9. Fund count by category
SELECT category, COUNT(*) AS total_funds
FROM dim_fund
GROUP BY category;

-- 10. Top NAV values
SELECT amfi_code, nav
FROM fact_nav
ORDER BY nav DESC
LIMIT 10;