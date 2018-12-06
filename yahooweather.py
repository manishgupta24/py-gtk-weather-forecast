import requests
import sqlite3
from requests import Response
from typing import List, Tuple

from sqlite_wrapper import SqliteWrapper
from utils import get_woeid_from_link


class YahooWeather:
    """
    Yahoo Weather Api.
    """

    BASE_URI = "https://query.yahooapis.com/v1/public/yql"

    def __init__(self, sqlite_object: SqliteWrapper = SqliteWrapper()):
        super(YahooWeather, self).__init__()
        self.sqlite_object = sqlite_object

    def _call_(self, city_name: str) -> Response:
        yql = """SELECT * FROM weather.forecast WHERE woeid IN (SELECT woeid FROM geo.places(1) WHERE text="%s") AND u="c" """ % city_name
        query_params = {"format": "json", "q": yql}
        return requests.get(self.BASE_URI, params=query_params)

    def fetch_forecast(self, city_name: str) -> tuple:
        response = self._call_(city_name).json()
        if "error" in response:
            return (False, response["error"]["description"], None)
        if not response["query"]["count"]:
            return (False, "Invalid City Name", None)
        self._save_data_(response["query"]["results"]["channel"])
        chart_data = self._get_historical_data_(
            response["query"]["results"]["channel"]["location"]["city"])
        return (True, response, chart_data)

    def _save_data_(self, results: dict):
        values = []
        query = """INSERT INTO temp (city_name, country_name, woe_id, forecast_date, high_temp, low_temp, forecast) VALUES """
        if "item" in results:
            self.woe_id = get_woeid_from_link(results["link"])
            for data in results["item"]["forecast"]:
                values.append(
                    """("%s", "%s", "%s", "%s", "%s", "%s", "%s")""" %
                    (results["location"]["city"],
                     results["location"]["country"], self.woe_id, data["date"],
                     data["high"], data["low"], data["text"]))
        values = ",".join(values)
        self.sqlite_object.insert_rows(query + values)
        with open("proc_save_data.sql", "r") as sql_file:
            sql_query = sql_file.read()
            sqlite3.complete_statement(sql_query)
            self.sqlite_object.cursor.executescript(sql_query)

    def _get_historical_data_(self, city_name: str):
        query = """SELECT
            STRFTIME("%m-%d", CAST(forecast_date AS DATE)), high_temp, low_temp
            FROM forecast INNER JOIN city on city.id = forecast.city_id
            WHERE city.woe_id = {0}
                AND city.city_name = "{1}"
            ORDER BY forecast_date; """.format(self.woe_id, city_name)
        rows = self.sqlite_object.fetch_all(query)
        date_list = [each[0] for each in rows]
        high_list = [each[1] for each in rows]
        low_list = [each[2] for each in rows]
        return (date_list, high_list, low_list)
