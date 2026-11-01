SET search_path = formula1, public;
COPY (SELECT json_agg(t) FROM (SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) as total_carreras,
  COUNT(DISTINCT id) as total_races_distinct
FROM race
WHERE year <= 2025
GROUP BY 1 ORDER BY 1) t) TO STDOUT;