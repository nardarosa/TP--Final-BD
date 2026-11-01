# -*- coding: utf-8 -*-
import subprocess, os

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'

def run_query(sql):
    with open('tmp_query.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_query.sql'], env=env, capture_output=True, text=True)
    return res.stdout

print("=== SCHEMAS ===")
print(run_query("SELECT table_schema, table_name FROM information_schema.tables WHERE table_name LIKE '%race%';"))
print(run_query("SHOW search_path;"))
