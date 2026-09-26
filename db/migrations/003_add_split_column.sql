ALTER TABLE sensor_readings
ADD COLUMN split TEXT CHECK (split IN ('train', 'val', 'test'));