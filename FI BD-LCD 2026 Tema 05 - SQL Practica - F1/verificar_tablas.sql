-- Cuenta la cantidad de registro por tabla de un esquema
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
        WHERE schemaname = 'formula1' --> agregar el nombre del esquema
    LOOP
        EXECUTE format(
            'SELECT COUNT(*) FROM %I.%I',
            'formula1', --> agregar el nombre del esquema
            r.tablename
        )
        INTO cantidad;

        INSERT INTO temp_conteo_tablas
        VALUES (r.tablename, cantidad);
    END LOOP;
END $$;


-- Lista las tablas y la cantidad de registros
SELECT *
FROM temp_conteo_tablas
ORDER BY registros DESC;