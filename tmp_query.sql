
    SET search_path = formula1, public;
    SELECT json_agg(t) FROM (WITH pole_decada AS (
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
ORDER BY decada) t;
    