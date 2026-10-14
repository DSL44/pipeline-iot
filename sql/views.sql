
-- View 1: Temperatura média por dispositivo
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp
FROM temperature_readings
GROUP BY device_id;

-- View 2: Quantidade de leituras por hora do dia
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date)::integer AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_date)
ORDER BY hora;

-- View 3: Temperaturas máxima e mínima por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    CAST(noted_date AS date) AS data,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY CAST(noted_date AS date)
ORDER BY data;
