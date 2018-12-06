import sys

import gi

# Check Gtk & Gdk Version before import
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

# All imports
from gi.repository import Gdk, Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from yahooweather import YahooWeather


class WeatherForecastApplicationBuilder(Gtk.Builder):
    def __init__(self, *args, **kwargs):
        Gtk.Builder.__init__(self, *args, **kwargs)
        self.add_from_file("layout.glade")
        self.window = self.get_object("WeatherForecastWindow")

        self._get_widgets_()
        self.connect_signals(self)
        self.window.show_all()
        Gtk.main()

    def _get_widgets_(self):
        # Define all Widgets Here
        self.city_name_search = self.get_object("CityNameSearch")

        # Values & Charts Widgets
        self.value_condition = self.get_object("ValueCondition")
        self.value_current_temp = self.get_object("ValueCurrentTemp")
        self.value_humidity = self.get_object("ValueHumidity")
        self.value_pressure = self.get_object("ValuePressure")

        # Graph Window
        self.graph_window = self.get_object("GraphWindow")

    def on_destroy(self, *args, **kwargs):
        Gtk.main_quit()

    def on_citynamesearch_change(self, event, *args, **kwargs):
        self._get_data_()

    def _get_data_(self):
        city_name = self.city_name_search.get_text()
        status, response, chart_data = YahooWeather().fetch_forecast(city_name)
        self._hide_data_()
        if status:
            self.show_data(response["query"]["results"]["channel"], chart_data)

    def show_data(self, response: dict, chart_data: tuple):
        self.value_humidity.set_text(response["atmosphere"]["humidity"])
        self.value_pressure.set_text(response["atmosphere"]["pressure"])
        self.value_condition.set_text(response["item"]["condition"]["text"])
        self.value_current_temp.set_text(response["item"]["condition"]["temp"])

        self._draw_chart_(chart_data)

    def _hide_data_(self):
        self.value_humidity.set_text("")
        self.value_pressure.set_text("")
        self.value_condition.set_text("")
        self.value_current_temp.set_text("")
        if self.graph_window.get_child():
            self.graph_window.remove(self.graph_window.get_child())

    def _draw_chart_(self, chart_data: tuple):
        figure = Figure()
        subplot = figure.add_subplot(111)
        subplot.plot(chart_data[0], chart_data[1])
        subplot.plot(chart_data[0], chart_data[2])
        subplot.set(xlabel='Date', ylabel='Temp', title='Temprature Change')

        canvas = FigureCanvas(figure)
        self.graph_window.add(canvas)
        self.window.show_all()


if __name__ == "__main__":
    WeatherForecastApplicationBuilder()