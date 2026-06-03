SELECT * FROM fact_nav LIMIT 10;

SELECT AVG(nav)
FROM fact_nav;

SELECT amfi_code, MAX(nav)
FROM fact_nav
GROUP BY amfi_code;