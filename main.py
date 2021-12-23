from utils.gps_utils import initialize_data, get_nearest_point, get_position_data
from utils.weather_utils import get_weather
import logging
from time import sleep
import os
from sys import exit
from gps import *

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                    level=logging.INFO)

try:
    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
except ConnectionRefusedError:
    logging.error("Cannot connect to GPS")

points = None
# TODO: Think a better idea than using this initial variable to None
initial_coord = None

# Base steps
# Obtain GPS Position
# Get nearest Village/City available by Haversine formula, get nearest from the two options.
# Telegram Bot interaction by commands. Commands available:
# /weather
# /tram or /bus to take neares tram/bus stop and retrieve times for all the available options
# /train destination -> Here, we need to check first the nearest station for the train. After that, scrape the data from the right
# webpage
#
# /restaurants keyword -> Here keyword will be the type of meal that you want. Ex: burger, sushi, etc. And obtain nearest one and best rated.
# /entertainment keyword -> Here you can specify some specific keywords. Ex: cinema, museum, etc. And obtain nearest one and best rated.

# Sample call for weather: https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=apiKeyHere

if __name__ == "__main__":
    while initial_coord is None:
        initial_coord = get_position_data(gpsd)
        sleep(0.5)

    openweather_api_key = os.environ.get('WEATHER_API_KEY')
    if not openweather_api_key:
        logging.error("Please, provide API Key on env var: WEATHER_API_KEY")
        exit(1)

    if points is None:
        logging.info(
            "Coord list is empty... Loading cities/villages data on mem...")
        points = initialize_data()

    # testing_point = {'lat': 41.97725783602381, 'lon': -4.935274927979529}
    coord_point = {'lat': initial_coord['lat'], 'lon': initial_coord['lon']}
    nearest_city = get_nearest_point(points.get('cities'), coord_point)
    nearest_village = get_nearest_point(points.get('villages'), coord_point)

    # TODO: Implement the "use nearest location to point" for weather and extra data.
    resp = get_weather(weather_api_key=openweather_api_key,
                       locations={
                           "city": nearest_city,
                           "village": nearest_village
                       },
                       location_country="es")
    if resp != None:
        logging.info(
            f"Weather: {resp.get('weather')}, location: {resp.get('name')}, temperatures: {resp.get('main')}"
        )
    else:
        logging.error("Error retrieving weather")
