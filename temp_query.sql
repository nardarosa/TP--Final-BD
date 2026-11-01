SET search_path = formula1;

SELECT reason_retired, COUNT(*) AS n,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(), 2) AS pct
FROM race_result
WHERE reason_retired IS NOT NULL
GROUP BY reason_retired
ORDER BY n DESC
LIMIT 40;
