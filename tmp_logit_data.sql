
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
