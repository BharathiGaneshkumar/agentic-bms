-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. sensor_readings: raw hourly AHU data, no FKs
CREATE TABLE sensor_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ahu_id TEXT NOT NULL,
    reading_time TIMESTAMP NOT NULL,
    set_point_temp NUMERIC,
    return_temp NUMERIC,
    supply_air_temp NUMERIC,
    supply_fan NUMERIC,
    valve_position NUMERIC,
    heating_supply_temp_1 NUMERIC,
    heating_supply_temp_2 NUMERIC,
    total_heating_pump NUMERIC,
    heating_pump_1 NUMERIC,
    heating_pump_2 NUMERIC,
    heating_pump_3 NUMERIC,
    cooling_supply_temp_1 NUMERIC,
    cooling_supply_temp_2 NUMERIC,
    total_cooling_pump NUMERIC,
    cooling_pump_1 NUMERIC,
    cooling_pump_2 NUMERIC,
    cooling_pump_3 NUMERIC,
    cooling_pump_4 NUMERIC,
    labeling TEXT NOT NULL
);

CREATE INDEX idx_sensor_readings_ahu_time ON sensor_readings (ahu_id, reading_time);