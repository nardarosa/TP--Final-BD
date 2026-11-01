# -*- coding: utf-8 -*-
import subprocess, os

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'

def run_query(sql):
    full_sql = "SET search_path = formula1, public;\n" + sql
    with open('tmp_query.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_query.sql'], env=env, capture_output=True, text=True)
    return res.stdout

print("=== ENGINES POST 2011 ===")
print(run_query("""
SELECT em.name, count(*) as starts, 
       count(*) FILTER (WHERE rr.position_number = 1) as wins,
       count(*) FILTER (WHERE rr.position_number <= 3) as podiums
FROM race_result rr
JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
JOIN race r ON rr.race_id = r.id
WHERE r.year >= 2011 AND r.year <= 2025
GROUP BY em.name
ORDER BY wins DESC, starts DESC;
"""))

print("=== ALL HISTORICAL ENGINES WITH WINS ===")
print(run_query("""
SELECT em.name, count(*) as starts, 
       count(*) FILTER (WHERE rr.position_number = 1) as wins
FROM race_result rr
JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
JOIN race r ON rr.race_id = r.id
WHERE rr.position_number = 1 AND r.year <= 2025
GROUP BY em.name
ORDER BY wins DESC
LIMIT 30;
"""))
