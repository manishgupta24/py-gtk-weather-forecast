# Python 3 GTK 3+ Weather Forecast Application 

Purpose of this application is to provide an interface to display weather forecast.
Yahoo Weather API is used to fetch the weather data. The data is stored in a SQLITE database.

>Note: We are sqlite for demo purposes only. For production level application, a more sophisticated dbms like PostgreSQL can be used.

In the Temrature chart both the high and low temprature range are plotted.


##### Requirements:
* Python 3.5+
* Ubuntu Environment LTS 16.04 / 18.04


##### Installation:
- chmod +x install.sh
- ./install.sh (Install using sudo if permission denied error is raised.)
- env/bin/python main.py (or python main.py if virtualenv is activated)
- env/bin/python tests.py (For Running Tests)


This project only implements the basic functionality i.e. displays only the temperature forecast using sqlite.
A lot of optimizations can be done on data storage part. MultiThreading can be used to save and display data in parallel.
