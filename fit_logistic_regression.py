# -*- coding: utf-8 -*-
import subprocess, os, json, math

psql = r'C:\Program Files\PostgreSQL\18\bin\psql.exe'
env = os.environ.copy()
env['PGPASSWORD'] = '2050'

# Extract dataset for logistic regression
sql = """
SET search_path = formula1, public;
COPY (
  SELECT
    CASE WHEN rr.position_number = 1 THEN 1 ELSE 0 END AS y_win,
    CASE WHEN rr.grid_position_number = 1 THEN 1 ELSE 0 END AS x_pole,
    CASE WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 1 ELSE 0 END AS x_p2p3,
    CASE WHEN r.year >= 2011 THEN 1 ELSE 0 END AS x_modern,
    CASE WHEN (rr.grid_position_number = 1 AND r.year >= 2011) THEN 1 ELSE 0 END AS x_pole_modern,
    CASE WHEN c.name IN ('Ferrari', 'McLaren', 'Mercedes', 'Red Bull', 'Williams') THEN 1 ELSE 0 END AS x_top_team
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  WHERE rr.grid_position_number IS NOT NULL AND r.year <= 2025
) TO STDOUT WITH CSV HEADER;
"""
with open('tmp_logit_data.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

res = subprocess.run([psql, '-U', 'postgres', '-d', 'postgres', '-f', 'tmp_logit_data.sql'], env=env, capture_output=True, text=True)
lines = res.stdout.strip().split('\n')
data_lines = [l.strip() for l in lines if l.strip() and not l.startswith('SET') and not l.startswith('y_win')]
rows = [list(map(int, line.split(','))) for line in data_lines]

print(f"Loaded {len(rows)} observations for logistic regression.")

# Simple Newton-Raphson or SGD for Logistic Regression
# Features: [Intercept, x_pole, x_p2p3, x_modern, x_top_team, x_pole_modern]
import numpy as np

X = np.array([[1] + r[1:] for r in rows], dtype=float)
y = np.array([r[0] for r in rows], dtype=float)

# Fit logistic regression with IRLS
beta = np.zeros(X.shape[1])
for iteration in range(25):
    p = 1.0 / (1.0 + np.exp(-np.clip(X @ beta, -30, 30)))
    W = p * (1.0 - p)
    # Gradient
    grad = X.T @ (y - p)
    # Hessian
    H = X.T @ (X * W[:, None])
    # Regularization for numerical stability
    H += np.eye(X.shape[1]) * 1e-4
    delta = np.linalg.solve(H, grad)
    beta += delta
    if np.max(np.abs(delta)) < 1e-6:
        print(f"Converged in {iteration+1} iterations!")
        break

# Compute standard errors from covariance matrix (inverse Hessian)
p = 1.0 / (1.0 + np.exp(-np.clip(X @ beta, -30, 30)))
W = p * (1.0 - p)
H = X.T @ (X * W[:, None])
cov = np.linalg.inv(H)
se = np.sqrt(np.diag(cov))
z_scores = beta / se
from scipy.stats import norm
p_values = [2 * (1 - norm.cdf(abs(z))) for z in z_scores]

feature_names = ['Intercept', 'Pole Position (P1)', 'Grilla P2-P3', 'Era Moderna (2011+)', 'Top Team (Constructor Líder)', 'Interacción: Pole × Era Moderna']
logit_results = []
for name, b, s, z, pval in zip(feature_names, beta, se, z_scores, p_values):
    odds_ratio = math.exp(b)
    logit_results.append({
        'variable': name,
        'coef': round(b, 4),
        'std_err': round(s, 4),
        'z_stat': round(z, 2),
        'p_value': "< 0.0001" if pval < 0.0001 else f"{pval:.4f}",
        'odds_ratio': round(odds_ratio, 2)
    })

print(json.dumps(logit_results, indent=2))
with open('logit_results.json', 'w', encoding='utf-8') as f:
    json.dump(logit_results, f, indent=2)
