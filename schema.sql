CREATE TABLE IF NOT EXISTS
    temp (
        city_name TEXT NOT NULL,
        country_name TEXT NOT NULL,
        woe_id TEXT NOT NULL,
        forecast_date TEXT NOT NULL,
        high_temp TEXT NOT NULL,
        low_temp TEXT NOT NULL,
        forecast TEXT NOT NULL
    );


CREATE TABLE IF NOT EXISTS 
    city (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_name TEXT NOT NULL,
        country_name TEXT NOT NULL,
        woe_id INTEGER NOT NULL
    );


CREATE TABLE IF NOT EXISTS
    forecast (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER NOT NULL,
        forecast_date TEXT NOT NULL,
        high_temp INTEGER NOT NULL,
        low_temp INTEGER NOT NULL,
        forecast TEXT NOT NULL,
        UNIQUE (city_id, forecast_date) ON CONFLICT REPLACE,
        FOREIGN KEY(city_id) REFERENCES city(id)
    );