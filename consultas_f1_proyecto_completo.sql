/* ==============================================================================
   PROYECTO: Las eras de la Fórmula 1 — Análisis SQL Completo
   AUTORES: Rosa, Kimel, Connon
   ASIGNATURA: Base de Datos — Licenciatura en Ciencia de Datos
   MOTOR: PostgreSQL 16+
   DESCRIPCIÓN: Compendio unificado de todas las consultas SQL desarrolladas a
                lo largo del proyecto (Fase EDA, Ejes Analíticos I al V,
                consultas auditadas de 2da/3ra entrega y dataset del modelo).
   ============================================================================== */

-- Configuración del entorno de trabajo
SET search_path = formula1, public;
SET client_encoding = 'UTF8';


-- ==============================================================================
-- 00. VERIFICACIÓN Y AUDITORÍA DE TABLAS
-- ==============================================================================

-- 00.1 Conteo de filas de todas las tablas del esquema formula1
DO $$
DECLARE
    r RECORD;
    cantidad BIGINT;
BEGIN
    DROP TABLE IF EXISTS temp_conteo_tablas;
    CREATE TEMP TABLE temp_conteo_tablas (
        tabla TEXT,
        registros BIGINT
    );

    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'formula1'
    LOOP
        EXECUTE format('SELECT COUNT(*) FROM %I.%I', 'formula1', r.tablename)
        INTO cantidad;

        INSERT INTO temp_conteo_tablas VALUES (r.tablename, cantidad);
    END LOOP;
END $$;

SELECT tabla, registros
FROM temp_conteo_tablas
ORDER BY registros DESC;


-- ==============================================================================
-- 01. FASE EXPLORATORIA (EDA - ENTREGA 1)
-- ==============================================================================

-- E01: Volumen de datos estimados en catálogo
SELECT
    t.table_name,
    c.reltuples::bigint AS filas_estimadas
FROM information_schema.tables t
JOIN pg_class c ON c.relname = t.table_name
WHERE t.table_schema = 'public'
  AND t.table_type = 'BASE TABLE'
ORDER BY filas_estimadas DESC;

-- E02: Desambiguación de tipos de sesión en la tabla race_data
SELECT
    type AS tipo_sesion,
    COUNT(*) AS filas,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_total
FROM race_data
GROUP BY type
ORDER BY filas DESC;

-- E03: Auditoría de integridad referencial (huérfanos en race_result)
SELECT
    COUNT(rr.race_id) AS resultados_totales,
    COUNT(r.id) AS con_carrera_valida,
    COUNT(rr.race_id) - COUNT(r.id) AS huerfanos_sin_carrera,
    COUNT(d.id) AS con_driver_valido,
    COUNT(rr.race_id) - COUNT(d.id) AS huerfanos_sin_driver
FROM race_result rr
LEFT JOIN race r ON r.id = rr.race_id
LEFT JOIN driver d ON d.id = rr.driver_id;

-- E04: Cobertura histórica y porcentaje de valores nulos (NULLs)
SELECT
    COUNT(*) AS total_filas,
    MIN(r.year) AS primer_anio,
    MAX(r.year) AS ultimo_anio,
    SUM(CASE WHEN rr.grid_position_number IS NULL THEN 1 ELSE 0 END) AS null_grilla,
    SUM(CASE WHEN rr.engine_manufacturer_id IS NULL THEN 1 ELSE 0 END) AS null_motor,
    ROUND(SUM(CASE WHEN rr.grid_position_number IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_null_grilla
FROM race_result rr
JOIN race r ON rr.race_id = r.id;

-- E05: Evolución del tamaño del campeonato (carreras por año y década)
SELECT
    year,
    COUNT(*) AS carreras_en_temporada,
    (year / 10) * 10 AS decada
FROM race
GROUP BY year
ORDER BY year;

-- E06: Concentración histórica preliminar de victorias por constructor por década
WITH wins_by_decade AS (
    SELECT
        (r.year / 10) * 10 AS decada,
        rr.constructor_id,
        COUNT(*) AS victorias
    FROM race_result rr
    JOIN race r ON rr.race_id = r.id
    WHERE rr.position_number = 1
    GROUP BY decada, rr.constructor_id
)
SELECT
    decada,
    constructor_id AS lider,
    victorias,
    ROUND(victorias * 100.0 / SUM(victorias) OVER (PARTITION BY decada), 1) AS pct_decada
FROM wins_by_decade
WHERE victorias = (
    SELECT MAX(victorias)
    FROM wins_by_decade w2
    WHERE w2.decada = wins_by_decade.decada
)
ORDER BY decada;


-- ==============================================================================
-- 02. EJE ANALÍTICO I: POSICIÓN DE SALIDA Y CONVERSIÓN EN CARRERA
-- ==============================================================================

-- Q01: Distribución histórica de victorias por posición de largada (1950-2025, Top 10)
SELECT
    rr.grid_position_number AS grilla,
    COUNT(*) AS victorias,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_victorias
FROM race_result rr
JOIN race r ON rr.race_id = r.id
WHERE rr.position_number = 1
  AND rr.grid_position_number IS NOT NULL
  AND r.year <= 2025
GROUP BY rr.grid_position_number
ORDER BY rr.grid_position_number
LIMIT 10;

-- Q02: Probabilidad condicional de victoria y podio por franja de grilla y por era
WITH clasif AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2–P3'
      WHEN rr.grid_position_number BETWEEN 4 AND 6 THEN 'P4–P6'
      WHEN rr.grid_position_number BETWEEN 7 AND 10 THEN 'P7–P10'
      ELSE 'P11+'
    END AS franja,
    CASE
      WHEN rr.grid_position_number = 1 THEN 1
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 2
      WHEN rr.grid_position_number BETWEEN 4 AND 6 THEN 3
      WHEN rr.grid_position_number BETWEEN 7 AND 10 THEN 4
      ELSE 5
    END AS orden_franja,
    rr.position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number IS NOT NULL AND r.year <= 2025
)
SELECT
  era, franja,
  COUNT(*) AS participaciones,
  COUNT(*) FILTER (WHERE position_number = 1) AS victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) AS pct_victoria,
  COUNT(*) FILTER (WHERE position_number <= 3) AS podios,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number <= 3) / COUNT(*), 2) AS pct_podio
FROM clasif
GROUP BY era, franja, orden_franja
ORDER BY era, orden_franja;

-- Q03: Cruce longitudinal de conversión de pole vs confiabilidad mecánica por década
WITH decade_stats AS (
  SELECT
    (r.year / 10) * 10 AS decada,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS total_poles,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) AS victorias_pole,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NULL) AS poles_terminaron,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.reason_retired IS NOT NULL) AS poles_abandonaron,
    COUNT(*) AS total_participaciones,
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
FROM decade_stats
ORDER BY decada;


-- ==============================================================================
-- 03. EJE ANALÍTICO II: COMPETITIVIDAD Y CONCENTRACIÓN LONGITUDINAL
-- ==============================================================================

-- Q04: Índice Herfindahl-Hirschman (HHI) anual de constructores promediado por era
WITH season_shares AS (
  SELECT
    r.year,
    rr.constructor_id,
    COUNT(*) AS wins,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY r.year) AS share
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year, rr.constructor_id
),
season_hhi AS (
  SELECT
    year,
    COUNT(DISTINCT constructor_id) AS constructores_ganadores,
    ROUND(SUM(POWER(share * 100, 2))::numeric, 1) AS hhi_season,
    MAX(share * 100) AS max_share_season
  FROM season_shares
  GROUP BY year
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
    ELSE '3. Híbrida (2014-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  ROUND(AVG(constructores_ganadores), 2) AS prom_constructores_ganadores,
  ROUND(AVG(max_share_season), 2) AS prom_share_lider_anual,
  ROUND(AVG(hhi_season), 1) AS prom_hhi_anual,
  MIN(hhi_season) AS min_hhi_anual,
  MAX(hhi_season) AS max_hhi_anual
FROM season_hhi
GROUP BY 1
ORDER BY 1;

-- Q08: Concentración de victorias en pilotos: % del máximo ganador y HHI anual
WITH season_driver_wins AS (
  SELECT
    r.year,
    rr.driver_id,
    COUNT(*) AS wins,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY r.year) AS win_share,
    SUM(COUNT(*)) OVER (PARTITION BY r.year) AS total_races
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year, rr.driver_id
),
season_driver_metrics AS (
  SELECT
    year,
    MAX(total_races) AS total_races,
    COUNT(DISTINCT driver_id) AS ganadores_distintos,
    MAX(win_share * 100) AS max_share_piloto,
    ROUND(SUM(POWER(win_share * 100, 2))::numeric, 1) AS hhi_pilotos
  FROM season_driver_wins
  GROUP BY year
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
    ELSE '3. Híbrida (2014-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  ROUND(AVG(ganadores_distintos), 2) AS prom_ganadores_temporada,
  ROUND(AVG(total_races), 1) AS prom_carreras,
  ROUND(AVG(max_share_piloto), 2) AS prom_share_max_ganador,
  ROUND(AVG(hhi_pilotos), 1) AS prom_hhi_pilotos,
  MIN(hhi_pilotos) AS min_hhi_pilotos,
  MAX(hhi_pilotos) AS max_hhi_pilotos
FROM season_driver_metrics
GROUP BY 1
ORDER BY 1;


-- ==============================================================================
-- 04. EJE ANALÍTICO III: HEGEMONÍA DEL MOTOR Y AISLAMIENTO OFICIAL VS CLIENTE
-- ==============================================================================

-- Q05: Cuota de victorias por familia de motor unificada (Rebadging comercial mapeado)
WITH engine_family AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2013 THEN '2. Intermedia (1981-2013)'
      ELSE '3. Híbrida (2014-2025)'
    END AS era,
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'Mugen-Honda') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer', 'Mecachrome', 'Playlife', 'Supertec') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name IN ('Ford', 'Cosworth') THEN 'Ford / Cosworth'
      WHEN em.name IN ('Ferrari', 'Petronas', 'Acer') THEN 'Ferrari'
      WHEN em.name IN ('TAG', 'Porsche') THEN 'Porsche / TAG'
      WHEN em.name IN ('BMW', 'Megatron') THEN 'BMW'
      ELSE em.name
    END AS familia_motor,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, familia_motor
),
totals AS (
  SELECT era, SUM(victorias) AS total_era FROM engine_family GROUP BY era
)
SELECT
  ef.era,
  ROW_NUMBER() OVER (PARTITION BY ef.era ORDER BY ef.victorias DESC) AS rk,
  ef.familia_motor,
  ef.victorias,
  ROUND(100.0 * ef.victorias / t.total_era, 2) AS pct_era
FROM engine_family ef
JOIN totals t ON ef.era = t.era
ORDER BY ef.era, rk;

-- Q06: Tasa de victoria y podio por participación efectiva de familia de motor (>= 50 GPs)
WITH base AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
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
)
SELECT
  era,
  ROW_NUMBER() OVER (PARTITION BY era ORDER BY victorias DESC) as rk,
  familia_motor, participaciones, victorias,
  ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
  podios,
  ROUND(100.0 * podios / participaciones, 2) AS pct_podio
FROM base
WHERE participaciones >= 50
ORDER BY era, rk;

-- Q07: Comparación intra-motor: Equipos Oficiales / Principales vs Equipos Clientes (2011-2025)
WITH base AS (
  SELECT
    CASE
      WHEN em.name IN ('Honda', 'Honda RBPT', 'RBPT') THEN 'Honda / RBPT'
      WHEN em.name IN ('Renault', 'TAG Heuer') THEN 'Renault / TAG Heuer'
      WHEN em.name IN ('Mercedes', 'BWT Mercedes') THEN 'Mercedes'
      WHEN em.name = 'Ferrari' THEN 'Ferrari'
      ELSE em.name
    END AS familia_motor,
    c.name AS constructor,
    CASE
      WHEN (em.name = 'Mercedes' AND c.name = 'Mercedes') OR
           (em.name = 'Ferrari' AND c.name = 'Ferrari') OR
           (em.name = 'Renault' AND c.name IN ('Renault', 'Alpine', 'Lotus')) OR
           (em.name IN ('Honda', 'Honda RBPT', 'RBPT', 'TAG Heuer') AND c.name = 'Red Bull')
      THEN 'Equipo Oficial / Principal'
      ELSE 'Equipo Cliente / Secundario'
    END AS tipo_equipo,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2-P3'
      ELSE 'P4+'
    END AS franja_grilla,
    rr.position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  JOIN constructor c ON rr.constructor_id = c.id
  WHERE r.year BETWEEN 2011 AND 2025 AND rr.grid_position_number IS NOT NULL
)
SELECT
  familia_motor,
  tipo_equipo,
  COUNT(*) as participaciones,
  COUNT(*) FILTER (WHERE position_number = 1) as victorias,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) as pct_victoria_total,
  COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)') as poles,
  COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)' AND position_number = 1) as vic_desde_pole,
  ROUND(100.0 * COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)' AND position_number = 1) / 
        NULLIF(COUNT(*) FILTER (WHERE franja_grilla = 'P1 (Pole)'), 0), 2) as conversion_pole_pct
FROM base
WHERE familia_motor IN ('Mercedes', 'Honda / RBPT', 'Ferrari', 'Renault / TAG Heuer')
GROUP BY familia_motor, tipo_equipo
ORDER BY familia_motor, tipo_equipo;


-- ==============================================================================
-- 05. EJE ANALÍTICO IV: CAMPEONES, CONFIABILIDAD Y SESGO CONDICIONAL
-- ==============================================================================

-- Q09: Porcentaje de victorias desde Pole de los campeones del mundo en su año de título
WITH campeon_año AS (
  SELECT year, driver_id
  FROM season_driver_standing
  WHERE championship_won = TRUE AND year <= 2025
),
victorias_campeon AS (
  SELECT
    c.year,
    c.driver_id,
    COUNT(*) AS vic_campeon,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS vic_desde_pole
  FROM campeon_año c
  JOIN race r ON r.year = c.year
  JOIN race_result rr ON rr.race_id = r.id AND rr.driver_id = c.driver_id
  WHERE rr.position_number = 1
  GROUP BY c.year, c.driver_id
)
SELECT
  CASE
    WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
    WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
    ELSE '3. Moderna (2011-2025)'
  END AS era,
  COUNT(*) AS temporadas,
  SUM(vic_campeon) AS total_victorias_campeones,
  SUM(vic_desde_pole) AS victorias_desde_pole,
  ROUND(100.0 * SUM(vic_desde_pole) / NULLIF(SUM(vic_campeon), 0), 2) AS pct_desde_pole
FROM victorias_campeon
GROUP BY era
ORDER BY era;

-- Q10: Conversión bruta de Pole vs Conversión condicional a cruzar la meta
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
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) as conversion_bruta_pct,
  COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) as abandonos_poleman,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reason_retired IS NOT NULL) / COUNT(*), 2) as pct_abandono_poleman,
  COUNT(*) FILTER (WHERE reason_retired IS NULL) as poles_terminaron,
  COUNT(*) FILTER (WHERE reason_retired IS NULL AND position_number = 1) as victorias_si_termina,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reason_retired IS NULL AND position_number = 1) / 
        NULLIF(COUNT(*) FILTER (WHERE reason_retired IS NULL), 0), 2) as conversion_si_termina_pct
FROM pole_data
GROUP BY era
ORDER BY era;

-- Q11: Taxonomía moderna de retiros: mecánica pura vs accidentes vs otros motivos
WITH clasif_retiros AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.reason_retired,
    CASE
      WHEN rr.reason_retired IS NULL THEN 'Finalizo'
      WHEN rr.reason_retired IN (
        'Engine', 'Gearbox', 'Electrical', 'Transmission', 'Suspension', 
        'Brakes', 'Clutch', 'Hydraulics', 'Fuel system', 'Turbo', 
        'Overheating', 'Ignition', 'Oil leak', 'Throttle', 
        'Radiator', 'Exhaust', 'Water pressure', 'Oil pressure', 'Battery',
        'Power Unit', 'ERS', 'Power loss', 'Electronics', 'Hybrid system',
        'Energy storage system failure', 'KERS failure', 'Differential', 'Driveshaft',
        'Cooling system', 'Coolant leak', 'Turbocharger', 'Fuel pressure', 'Fuel leak',
        'Technical defect', 'Mechenical', 'Water leak', 'Pneumatics', 'Alternator',
        'Halfshaft', 'Wheel bearing', 'Driveshaft hub', 'Fuel pump', 'Oil pump'
      ) THEN 'Averia Mecanica'
      WHEN rr.reason_retired IN (
        'Accident', 'Collision', 'Spun off', 'Collision damage', 'Damage', 
        'Fatal accident', 'Car damaged', 'Accident in warm-up', 'Accident on formation lap'
      ) THEN 'Accidente/Colision'
      ELSE 'Otro Abandono'
    END AS categoria_retiro
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025
)
SELECT
  era,
  COUNT(*) AS total_participaciones,
  COUNT(*) FILTER (WHERE categoria_retiro != 'Finalizo') AS total_abandonos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro != 'Finalizo') / COUNT(*), 2) AS pct_abandono_total,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Averia Mecanica') AS abandonos_mecanicos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Averia Mecanica') / COUNT(*), 2) AS pct_abandono_mecanico,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Accidente/Colision') AS accidentes,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Accidente/Colision') / COUNT(*), 2) AS pct_accidentes,
  COUNT(*) FILTER (WHERE categoria_retiro = 'Otro Abandono') AS otros_abandonos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE categoria_retiro = 'Otro Abandono') / COUNT(*), 2) AS pct_otros
FROM clasif_retiros
GROUP BY era
ORDER BY era;


-- ==============================================================================
-- 06. EJE ANALÍTICO V: EL FACTOR HUMANO (COMPAÑEROS Y DELTAS)
-- ==============================================================================

-- Q12: Brecha sistemática entre compañeros de equipo (>=10 carreras compartidas)
WITH pares_temporada AS (
  SELECT
    r.year, rr.constructor_id, c.name AS constructor_name,
    rr.driver_id, d.name AS driver_name,
    COUNT(*) AS carreras,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    SUM(COALESCE(rr.points, 0)) AS puntos
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  JOIN driver d ON rr.driver_id = d.id
  WHERE r.year <= 2025
  GROUP BY r.year, rr.constructor_id, c.name, rr.driver_id, d.name
  HAVING COUNT(*) >= 10
),
constructor_seasons AS (
  SELECT
    year, constructor_name,
    MAX(puntos) AS max_puntos, MIN(puntos) AS min_puntos,
    MAX(victorias) AS max_vic, SUM(puntos) AS tot_puntos, SUM(victorias) AS tot_vic
  FROM pares_temporada
  GROUP BY year, constructor_id, constructor_name
  HAVING COUNT(*) = 2
),
brechas AS (
  SELECT
    year,
    CASE
      WHEN year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    CASE WHEN tot_puntos > 0 THEN ROUND(100.0 * (max_puntos - min_puntos) / tot_puntos, 2) ELSE 0 END AS brecha_puntos_pct,
    CASE WHEN tot_vic > 0 THEN ROUND(100.0 * max_vic / tot_vic, 2) ELSE 50.0 END AS pct_victorias_lider
  FROM constructor_seasons
)
SELECT
  era,
  COUNT(*) AS parejas_analizadas,
  ROUND(AVG(brecha_puntos_pct), 2) AS prom_brecha_puntos_pct,
  ROUND(AVG(pct_victorias_lider), 2) AS prom_share_vic_lider_pareja
FROM brechas
GROUP BY era
ORDER BY era;

-- A1: Delta de posiciones ganadas/perdidas y tasa de retención de puesto por era
WITH deltas AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    rr.grid_position_number, rr.position_number,
    (rr.grid_position_number - rr.position_number) AS pos_ganadas
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025 
    AND rr.grid_position_number IS NOT NULL 
    AND rr.position_number IS NOT NULL
)
SELECT
  era,
  COUNT(*) AS total_finalizados,
  ROUND(AVG(pos_ganadas), 2) AS prom_pos_ganadas,
  COUNT(*) FILTER (WHERE pos_ganadas = 0) AS mantuvo_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas = 0) / COUNT(*), 2) AS pct_mantuvo_pos,
  COUNT(*) FILTER (WHERE pos_ganadas > 0) AS gano_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas > 0) / COUNT(*), 2) AS pct_gano_pos,
  COUNT(*) FILTER (WHERE pos_ganadas < 0) AS perdio_pos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE pos_ganadas < 0) / COUNT(*), 2) AS pct_perdio_pos
FROM deltas
GROUP BY era
ORDER BY era;


-- ==============================================================================
-- 07. DATASET PARA REGRESIÓN LOGÍSTICA (MODELADO MULTIVARIADO)
-- ==============================================================================

-- Extracción de variables dependientes e independientes para estimar odds ratios
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
WHERE rr.grid_position_number IS NOT NULL 
  AND r.year <= 2025;


-- ==============================================================================
-- 08. VARIANTES ORIGINALES DE LA 2DA ENTREGA (VERSIONES PREVIAS A LA AUDITORÍA)
-- ==============================================================================
-- Estas consultas corresponden a las formulaciones directas presentadas en la
-- 2da entrega antes de los refinamientos metodológicos aplicados en la 3ra entrega.

-- Q03_ORIGINAL: Conversión simple de Pole Position a Victoria agrupada por década
WITH poles_year AS (
  SELECT
    r.year,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS poles_largaron,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1 AND rr.position_number = 1) AS poles_ganaron
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.grid_position_number IS NOT NULL AND r.year <= 2025
  GROUP BY r.year
)
SELECT
  (year / 10) * 10 AS decada,
  SUM(poles_largaron) AS total_poles,
  SUM(poles_ganaron) AS victorias_desde_pole,
  ROUND(100.0 * SUM(poles_ganaron) / NULLIF(SUM(poles_largaron), 0), 2) AS tasa_conversion_pct
FROM poles_year
GROUP BY (year / 10) * 10
ORDER BY decada;

-- Q04_ORIGINAL: Índice Herfindahl-Hirschman (HHI) acumulado por era
WITH constructor_wins AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    c.name AS constructor_name,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, c.name
),
totals AS (
  SELECT era, SUM(victorias) AS total_victorias
  FROM constructor_wins
  GROUP BY era
),
shares AS (
  SELECT
    cw.era, cw.constructor_name, cw.victorias,
    ROUND(cw.victorias * 100.0 / t.total_victorias, 2) AS cuota_mercado_pct,
    POWER(cw.victorias * 100.0 / t.total_victorias, 2) AS cuota_al_cuadrado
  FROM constructor_wins cw
  JOIN totals t ON cw.era = t.era
)
SELECT
  era,
  COUNT(DISTINCT constructor_name) AS constructores_con_victoria,
  ROUND(SUM(cuota_al_cuadrado)::numeric, 1) AS indice_hhi
FROM shares
GROUP BY era
ORDER BY era;

-- Q05_ORIGINAL: Cuota de victorias por fabricante de motor directo (sin rebadging)
WITH motor_wins AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    em.name AS fabricante_motor,
    COUNT(*) AS victorias
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY era, em.name
),
totals AS (
  SELECT era, SUM(victorias) AS total_era FROM motor_wins GROUP BY era
)
SELECT
  mw.era,
  ROW_NUMBER() OVER (PARTITION BY mw.era ORDER BY mw.victorias DESC) AS rk,
  mw.fabricante_motor,
  mw.victorias,
  ROUND(100.0 * mw.victorias / t.total_era, 2) AS pct_era
FROM motor_wins mw
JOIN totals t ON mw.era = t.era
ORDER BY mw.era, rk;

-- Q07_ORIGINAL: Tasa de victoria de motores controlando por franja de grilla en Era Moderna (2011-2025)
WITH base AS (
  SELECT
    em.name AS motor,
    CASE
      WHEN rr.grid_position_number = 1 THEN 'P1 (Pole)'
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 'P2-P3'
      ELSE 'P4+'
    END AS franja_grilla,
    CASE
      WHEN rr.grid_position_number = 1 THEN 1
      WHEN rr.grid_position_number BETWEEN 2 AND 3 THEN 2
      ELSE 3
    END AS orden_franja,
    COUNT(*) AS participaciones,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  WHERE r.year BETWEEN 2011 AND 2025 AND rr.grid_position_number IS NOT NULL
  GROUP BY em.name, franja_grilla, orden_franja
)
SELECT
  franja_grilla,
  motor,
  participaciones,
  victorias,
  ROUND(100.0 * victorias / participaciones, 2) AS pct_victoria,
  podios,
  ROUND(100.0 * podios / participaciones, 2) AS pct_podio
FROM base
WHERE participaciones >= 15
ORDER BY orden_franja, pct_victoria DESC;

-- Q08_ORIGINAL: Promedio de pilotos ganadores distintos por temporada y ratio de apertura competitiva
WITH ganadores_temporada AS (
  SELECT
    r.year,
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    COUNT(DISTINCT rr.driver_id) AS pilotos_ganadores,
    COUNT(*) AS total_carreras
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE rr.position_number = 1 AND r.year <= 2025
  GROUP BY r.year
)
SELECT
  era,
  COUNT(*) AS temporadas,
  ROUND(AVG(pilotos_ganadores), 2) AS prom_ganadores_por_temporada,
  ROUND(AVG(total_carreras), 1) AS prom_carreras_por_temporada,
  ROUND(AVG(pilotos_ganadores * 1.0 / total_carreras), 3) AS ratio_apertura_promedio
FROM ganadores_temporada
GROUP BY era
ORDER BY era;

-- Q10_ORIGINAL: Tasa de conversión de pole en carreras decisivas de campeonato vs regulares
WITH clasif AS (
  SELECT
    CASE
      WHEN r.year BETWEEN 1950 AND 1980 THEN '1. Clásica (1950-1980)'
      WHEN r.year BETWEEN 1981 AND 2010 THEN '2. Intermedia (1981-2010)'
      ELSE '3. Moderna (2011-2025)'
    END AS era,
    r.drivers_championship_decider AS es_decisiva,
    rr.grid_position_number,
    rr.position_number
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  WHERE r.year <= 2025 AND rr.grid_position_number = 1 AND rr.position_number IS NOT NULL
)
SELECT
  era,
  CASE WHEN es_decisiva THEN 'Carrera Decisiva' ELSE 'Carrera Regular' END AS tipo_carrera,
  COUNT(*) AS total_poles,
  COUNT(*) FILTER (WHERE position_number = 1) AS victorias_desde_pole,
  ROUND(100.0 * COUNT(*) FILTER (WHERE position_number = 1) / COUNT(*), 2) AS tasa_conversion_pct
FROM clasif
GROUP BY era, es_decisiva
ORDER BY era, es_decisiva DESC;

-- Q12_ORIGINAL: Comparación intra-equipo en temporadas dominantes seleccionadas
WITH pares_clave AS (
  SELECT
    r.year,
    c.name AS constructor,
    em.name AS motor,
    d.name AS piloto,
    COUNT(*) AS carreras,
    COUNT(*) FILTER (WHERE rr.position_number = 1) AS victorias,
    COUNT(*) FILTER (WHERE rr.position_number <= 3) AS podios,
    COUNT(*) FILTER (WHERE rr.grid_position_number = 1) AS poles,
    ROUND(SUM(COALESCE(rr.points, 0)), 1) AS puntos
  FROM race_result rr
  JOIN race r ON rr.race_id = r.id
  JOIN constructor c ON rr.constructor_id = c.id
  JOIN engine_manufacturer em ON rr.engine_manufacturer_id = em.id
  JOIN driver d ON rr.driver_id = d.id
  WHERE (r.year IN (1988, 2002, 2014, 2016, 2021, 2023)
         AND c.name IN ('McLaren', 'Ferrari', 'Mercedes', 'Red Bull'))
  GROUP BY r.year, c.name, em.name, d.name
  HAVING COUNT(*) >= 10
)
SELECT year, constructor, motor, piloto, carreras, victorias, podios, poles, puntos
FROM pares_clave
ORDER BY year, constructor, victorias DESC, puntos DESC;
