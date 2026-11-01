# -*- coding: utf-8 -*-
import subprocess, os, json

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'
env['PGCLIENTENCODING'] = 'UTF8'

def q(sql):
    clean = sql.strip().rstrip(';')
    full_sql = f"""SET search_path = formula1, public;
COPY (SELECT json_agg(t) FROM ({clean}) t) TO STDOUT;"""
    with open('tmp_check.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_check.sql'], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    raw = res.stdout
    idx = raw.find('[')
    if idx != -1:
        raw = raw[idx:].strip().replace('\\n', ' ')
        return json.loads(raw)
    return []

print('=== 1. NULL GRIDS BY ERA ===')
print(json.dumps(q('''
SELECT
  CASE
    WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
    WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) as total_filas,
  COUNT(*) FILTER (WHERE rr.grid_position_number IS NOT NULL) as grilla_not_null,
  COUNT(*) FILTER (WHERE rr.grid_position_number IS NULL) as grilla_null,
  COUNT(*) FILTER (WHERE rr.position_number IS NOT NULL) as pos_not_null,
  COUNT(*) FILTER (WHERE rr.position_number IS NULL) as pos_null
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE r.year <= 2025
GROUP BY 1 ORDER BY 1;
'''), indent=2))

print('=== 2. WHY GRID IS NULL ===')
print(json.dumps(q('''
SELECT
  CASE
    WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
    WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  rr.position_text, rr.reason_retired, count(*) as cnt
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE rr.grid_position_number IS NULL AND r.year <= 2025
GROUP BY 1, 2, 3
ORDER BY era, cnt DESC
LIMIT 20;
'''), indent=2))

print('=== 3. POLE (grid_position_number = 1) POSITION_NUMBER NULLS ===')
print(json.dumps(q('''
SELECT
  CASE
    WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
    WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) FILTER (WHERE rr.grid_position_number = 1) as poles_totales_grilla_1,
  COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number IS NOT NULL) as poles_pos_not_null,
  COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number IS NULL) as poles_pos_null,
  COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) as poles_ganaron,
  COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NOT NULL) as poles_abandonaron
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE r.year <= 2025
GROUP BY 1 ORDER BY 1;
'''), indent=2))

print('=== 4. TOTAL RACES PER ERA (TOTAL POLES POSSIBLE = TOTAL RACES) ===')
print(json.dumps(q('''
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clasica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) as total_carreras,
  COUNT(DISTINCT id) as total_races_distinct
FROM race
WHERE year <= 2025
GROUP BY 1 ORDER BY 1;
'''), indent=2))
