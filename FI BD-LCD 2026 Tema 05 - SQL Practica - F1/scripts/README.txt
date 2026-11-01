F1DB PostgreSQL - SQL dividido para DBeaver
================================================

Ejecutar los archivos EN ORDEN por nombre.
Cada archivo de datos contiene como máximo 15.000 sentencias INSERT.
Cada archivo de datos usa BEGIN/COMMIT para confirmar el bloque.

Orden de ejecución:
1. 00_estructura.sql
- 01_continent.sql: 7 INSERT (continent)
- 02_country.sql: 249 INSERT (country)
- 03_driver.sql: 917 INSERT (driver)
- 04_driver_family_relationship.sql: 86 INSERT (driver_family_relationship)
- 05_constructor.sql: 187 INSERT (constructor)
- 06_constructor_chronology.sql: 217 INSERT (constructor_chronology)
- 07_chassis.sql: 1.153 INSERT (chassis)
- 08_engine_manufacturer.sql: 78 INSERT (engine_manufacturer)
- 09_engine.sql: 424 INSERT (engine)
- 10_tyre_manufacturer.sql: 9 INSERT (tyre_manufacturer)
- 11_entrant.sql: 830 INSERT (entrant)
- 12_circuit.sql: 78 INSERT (circuit)
- 13_circuit_layout.sql: 160 INSERT (circuit_layout)
- 14_grand_prix.sql: 54 INSERT (grand_prix)
- 15_season.sql: 77 INSERT (season)
- 16_season_entrant.sql: 1.799 INSERT (season_entrant)
- 17_season_entrant_constructor.sql: 1.925 INSERT (season_entrant_constructor)
- 18_season_entrant_chassis.sql: 2.292 INSERT (season_entrant_chassis)
- 19_season_entrant_engine.sql: 2.027 INSERT (season_entrant_engine)
- 20_season_entrant_tyre_manufacturer.sql: 1.955 INSERT (season_entrant_tyre_manufacturer)
- 21_season_entrant_driver.sql: 3.882 INSERT (season_entrant_driver)
- 22_season_constructor.sql: 1.079 INSERT (season_constructor)
- 23_season_engine_manufacturer.sql: 560 INSERT (season_engine_manufacturer)
- 24_season_tyre_manufacturer.sql: 160 INSERT (season_tyre_manufacturer)
- 25_season_driver.sql: 3.416 INSERT (season_driver)
- 26_season_driver_standing.sql: 1.681 INSERT (season_driver_standing)
- 27_season_constructor_standing.sql: 721 INSERT (season_constructor_standing)
- 28_race.sql: 1.172 INSERT (race)
- 29_race_data_01.sql: 15.000 INSERT (race_data)
- 30_race_data_02.sql: 15.000 INSERT (race_data)
- 31_race_data_03.sql: 15.000 INSERT (race_data)
- 32_race_data_04.sql: 15.000 INSERT (race_data)
- 33_race_data_05.sql: 15.000 INSERT (race_data)
- 34_race_data_06.sql: 15.000 INSERT (race_data)
- 35_race_data_07.sql: 15.000 INSERT (race_data)
- 36_race_data_08.sql: 15.000 INSERT (race_data)
- 37_race_data_09.sql: 15.000 INSERT (race_data)
- 38_race_data_10.sql: 15.000 INSERT (race_data)
- 39_race_data_11.sql: 15.000 INSERT (race_data)
- 40_race_data_12.sql: 15.000 INSERT (race_data)
- 41_race_data_13.sql: 7.138 INSERT (race_data)
- 42_race_driver_standing_01.sql: 15.000 INSERT (race_driver_standing)
- 43_race_driver_standing_02.sql: 6.472 INSERT (race_driver_standing)
- 44_race_constructor_standing.sql: 10.621 INSERT (race_constructor_standing)

Cantidad de registros por tabla:
- continent: 7
- country: 249
- driver: 917
- driver_family_relationship: 86
- constructor: 187
- constructor_chronology: 217
- chassis: 1.153
- engine_manufacturer: 78
- engine: 424
- tyre_manufacturer: 9
- entrant: 830
- circuit: 78
- circuit_layout: 160
- grand_prix: 54
- season: 77
- season_entrant: 1.799
- season_entrant_constructor: 1.925
- season_entrant_chassis: 2.292
- season_entrant_engine: 2.027
- season_entrant_tyre_manufacturer: 1.955
- season_entrant_driver: 3.882
- season_constructor: 1.079
- season_engine_manufacturer: 560
- season_tyre_manufacturer: 160
- season_driver: 3.416
- season_driver_standing: 1.681
- season_constructor_standing: 721
- race: 1.172
- race_data: 187.138
- race_driver_standing: 21.472
- race_constructor_standing: 10.621

TOTAL INSERT: 246.426
