SET search_path = formula1, public;
COPY (SELECT json_agg(t) FROM (WITH base AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
      WHEN em.name IN ('Ferrari', 'Petronas', 'Acer') THEN 'Ferrari'
      ELSE em.name
    END AS familia_motor,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year <= 2025
  GROUP BY era, familia_motor
),
ranked AS (
  SELECT
    era, familia_motor, participaciones, victorias,
    ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
    podios,
    ROUND(100.0 * podios / participaciones, 2) AS pct_podio,
    ROW_NUMBER() OVER (PARTITION BY era ORDER BY victorias DESC, participaciones DESC) as rk
  FROM base
  WHERE participaciones >= 50
)
SELECT era, rk, familia_motor, participaciones, victorias, pct_victoria, podios, pct_podio
FROM ranked
WHERE rk <= 5
ORDER BY era, rk) t) TO STDOUT;