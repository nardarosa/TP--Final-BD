# -*- coding: utf-8 -*-
import subprocess, os, json, math

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'

def run_query_json(sql):
    clean_sql = sql.strip().rstrip(';')
    full_sql = f"""
    SET search_path = formula1, public;
    SELECT json_agg(t) FROM ({clean_sql}) t;
    """
    with open('tmp_query.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-t', '-A', '-f', 'tmp_query.sql'], env=env, capture_output=True, text=True)
    if res.stderr and "ERROR" in res.stderr:
        print("STDERR ERROR:", res.stderr)
        return []
    out = res.stdout.strip()
    for line in out.split('\n'):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            return json.loads(line)
    return []

# Point 1: Engine rebadging mapping check
sql_engines = """
WITH remapped AS (
  SELECT
    r.year,
    em.name AS original_motor,
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
      WHEN em.name IN ('TAG', 'Porsche') THEN 'Porsche / TAG'
      WHEN em.name IN ('BMW', 'Megatron') THEN 'BMW'
      ELSE em.name
    END AS familia_motor,
    rr.position_number,
    rr.grid_position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year <= 2025
)
SELECT familia_motor,
       count(*) FILTER (WHERE position_number = 1) as wins_total,
       count(*) FILTER (WHERE position_number = 1 AND year BETWEEN 2011 AND 2025) as wins_moderna,
       count(*) FILTER (WHERE position_number = 1 AND year BETWEEN 2014 AND 2025) as wins_hybrid
FROM remapped
WHERE position_number = 1
GROUP BY familia_motor
ORDER BY wins_total DESC;
"""
print("--- ENGINE REBADGING MAPPING ---")
print(json.dumps(run_query_json(sql_engines), indent=2))

# Point 3: Hallazgo sin explotar en Q10: Pole -> Victoria condicionado a terminar
sql_pole_finish = """
WITH pole_data AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.position_number,
    rr.reason_retired
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number = 1 AND r.year <= 2025
)
SELECT
  era,
  COUNT(*) as total_poles,
  COUNT(*) FILTER (WHERE position_number = 1) as victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) as tasa_conversion_bruta,
  COUNT(*) FILTER (WHERE reason_retired IS NULL) as poles_terminaron,
  COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) as poles_abandonaron,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) / COUNT(*), 2) as pct_abandono_poleman,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / NULLIF(COUNT(*) FILTER (WHERE reason_retired IS NULL), 0), 2) as tasa_conversion_condicional_terminar
FROM pole_data
GROUP BY era
ORDER BY era;
"""
print("\n--- POLE CONVERSION CONDITIONED ON FINISHING ---")
print(json.dumps(run_query_json(sql_pole_finish), indent=2))

# Point 9: Cruzar confiabilidad por década con conversión de pole
sql_q03_cruzado = """
WITH pole_decada AS (
  SELECT
    (r.year / 10) * 10 AS decada,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS total_poles,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) AS victorias_pole,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NULL) AS poles_terminaron,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NOT NULL) AS poles_abandonaron,
    COUNT(*) AS total_participaciones,
    COUNT(*) FILTER (WHERE rr.reason_retired IS NOT NULL) AS total_abandonos,
    COUNT(*) FILTER (WHERE rr.reason_retired IN (
      'Engine', 'Gearbox', 'Electrical', 'Transmission', 'Suspension', 
      'Brakes', 'Clutch', 'Hydraulics', 'Fuel system', 'Turbo', 
      'Overheating', 'Ignition', 'Oil leak', 'Throttle', 
      'Radiator', 'Exhaust', 'Water pressure', 'Oil pressure', 'Battery',
      'Power Unit', 'ERS', 'Power loss', 'Electronics', 'Hybrid system',
      'Energy storage system failure', 'KERS failure', 'Differential', 'Driveshaft',
      'Cooling system', 'Coolant leak', 'Turbocharger', 'Fuel pressure', 'Fuel leak',
      'Technical defect', 'Mechenical'
    )) AS fallas_mecanicas
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025
  GROUP BY (r.year / 10) * 10
)
SELECT
  decada,
  total_poles,
  victorias_pole,
  ROUND(100.0 * victorias_pole / NULLIF(total_poles, 0), 2) AS tasa_conversion_pole,
  ROUND(100.0 * poles_abandonaron / NULLIF(total_poles, 0), 2) AS pct_abandono_poleman,
  ROUND(100.0 * victorias_pole / NULLIF(poles_terminaron, 0), 2) AS tasa_conversion_si_termina,
  ROUND(100.0 * fallas_mecanicas / NULLIF(total_participaciones, 0), 2) AS pct_falla_mecanica_global
FROM pole_decada
ORDER BY decada;
"""
print("\n--- DECADE POLE & RELIABILITY CROSSOVER ---")
print(json.dumps(run_query_json(sql_q03_cruzado), indent=2))
