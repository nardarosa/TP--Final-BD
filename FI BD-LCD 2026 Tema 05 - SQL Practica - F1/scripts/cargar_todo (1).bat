@echo off
chcp 65001 > nul
setlocal

set PSQL="C:\Program Files\PostgreSQL\18\bin\psql.exe"
set HOST=localhost
set PORT=5432
set DB=postgres
set USER=postgres
set PGPASSWORD=2050
set SCHEMA=formula1
set PGOPTIONS=--search_path=%SCHEMA%
set PGCLIENTENCODING=UTF8

echo.
echo Cargando base %DB%
echo.

for %%f in (*.sql) do (
    echo ----------------------------------------
    echo Ejecutando %%f
    echo ----------------------------------------

    %PSQL% -h %HOST% -p %PORT% -U %USER% -d %DB% -v ON_ERROR_STOP=1 -f "%%f"

    if errorlevel 1 (
        echo.
        echo ERROR EN: %%f
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo CARGA FINALIZADA CORRECTAMENTE
echo ========================================
pause