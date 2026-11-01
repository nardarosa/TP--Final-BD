# -*- coding: utf-8 -*-
import subprocess, os, json

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'

def run_query(sql):
    full_sql = "SET search_path = formula1, public;\n" + sql
    with open('tmp_query.sql', 'w', encoding='utf-8') as f:
        f.write(full_sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_query.sql'], env=env, capture_output=True, text=True)
    if res.stderr:
        print("STDERR:", res.stderr)
    return res.stdout

# 1. Audit retirement reasons in the DB
print("=== DISTINCT REASON RETIRED ===")
print(run_query("""
SELECT reason_retired, count(*) as cnt,
       count(*) FILTER (WHERE r.year >= 2014) as cnt_hybrid
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE rr.reason_retired IS NOT NULL
GROUP BY reason_retired
ORDER BY cnt_hybrid DESC, cnt DESC;
"""))
