# -*- coding: utf-8 -*-
import subprocess, os, json

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'
env['PGCLIENTENCODING'] = 'UTF8'

def run_sql(sql):
    clean = sql.strip().rstrip(';')
    full_sql = f"""SET search_path = formula1, public;
COPY (SELECT json_agg(t) FROM ({clean}) t) TO STDOUT;"""
    with open('tmp_step.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_step.sql'], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    raw = res.stdout
    idx = raw.find('[')
    if idx != -1:
        clean_json = raw[idx:].strip().replace('\\n', ' ')
        return json.loads(clean_json)
    return []

print("=== Q06 STANDARD ===")
data_std = run_sql("""
WITH base AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    em.name AS motor,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year <= 2025
  GROUP BY era, em.name
),
ranked AS (
  SELECT
    era, motor, participaciones, victorias,
    ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
    podios,
    ROUND(100.0 * podios / participaciones, 2) AS pct_podio,
    ROW_NUMBER() OVER (PARTITION BY era ORDER BY victorias DESC, participaciones DESC) as rk
  FROM base
  WHERE participaciones >= 50
)
SELECT era, rk, motor, participaciones, victorias, pct_victoria, podios, pct_podio
FROM ranked
WHERE rk <= 5
ORDER BY era, rk;
""")
print(json.dumps(data_std, indent=2))

print("=== Q06 REBADGED ===")
data_reb = run_sql("""
WITH base AS (
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
ORDER BY era, rk;
""")
print(json.dumps(data_reb, indent=2))
