DROP TABLE IF EXISTS sensor_data;

CREATE TABLE latest_10_minutes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    sensor TEXT,
    value DECIMAL(4,2)
)
CREATE TABLE latest_30_minutes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    sensor TEXT,
    value DECIMAL(4,2)
)