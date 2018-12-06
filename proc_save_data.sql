INSERT INTO city (city_name, country_name, woe_id)
	SELECT DISTINCT city_name, country_name, woe_id
		FROM temp
		WHERE NOT EXISTS (
			SELECT 1
			FROM city
			WHERE city.city_name = temp.city_name
				AND city.woe_id = temp.woe_id);


INSERT INTO forecast (city_id, forecast_date, high_temp, low_temp, forecast)
	SELECT city.id, temp.forecast_date, CAST(temp.high_temp AS INTEGER), CAST(temp.low_temp AS INTEGER), temp.forecast 
		FROM temp
		INNER JOIN city on city.woe_id = temp.woe_id
			AND city.city_name = temp.city_name;
