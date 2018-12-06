import os
import unittest

from yahooweather import YahooWeather
from sqlite_wrapper import SqliteWrapper


class YahooWeatherTest(unittest.TestCase):
    def setUp(self):
        self.sqlite_object = SqliteWrapper("forecast-test.db")

    def tearDown(self):
        os.remove("forecast-test.db")

    def test_valid(self):
        status, response, chart_data = YahooWeather(
            sqlite_object=self.sqlite_object).fetch_forecast("delhi")
        self.assertEqual(status, True)
        self.assertEqual(type(response), dict)
        self.assertNotEqual(chart_data, None)

    def test_invalid(self):
        status, response, chart_data = YahooWeather(
            sqlite_object=self.sqlite_object).fetch_forecast("versgehi")
        self.assertEqual(status, False)
        self.assertNotEqual(type(response), dict)
        self.assertEqual(response, "Invalid City Name")
        self.assertEqual(chart_data, None)

    def test_empty(self):
        status, response, chart_data = YahooWeather(
            sqlite_object=self.sqlite_object).fetch_forecast("")
        self.assertEqual(status, False)
        self.assertNotEqual(type(response), dict)
        self.assertEqual(response, "Empty text")
        self.assertEqual(chart_data, None)

    def test_save_data(self):
        status, response, chart_data = YahooWeather(
            sqlite_object=self.sqlite_object).fetch_forecast("delhi")
        row_count = self.sqlite_object.fetch_one(
            "Select Count(*) From forecast;")[0]
        self.assertEqual(
            row_count,
            len(response["query"]["results"]["channel"]["item"]["forecast"]))


if __name__ == '__main__':
    unittest.main()
