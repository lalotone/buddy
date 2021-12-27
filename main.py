from utils.gps_utils import load_data, get_nearest_point, get_position_data
from utils.weather_utils import get_weather
import logging
from time import sleep
import os
from sys import exit
from gps import *
from datetime import datetime

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                    level=logging.INFO)
openweather_api_key = os.environ.get('WEATHER_API_KEY')
    
try:
    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
except ConnectionRefusedError:
    logging.error("Cannot connect to GPS")
    
if not openweather_api_key:
        logging.error("Please, provide API Key on env var: WEATHER_API_KEY")
        exit(1)

points = None
current_date = datetime.now()

# TODO: Think a better idea than using this initial variable to None
run = True

# TODO: Move this variables to a config file
# Refresh rate: In seconds, to retrieve latest position
refresh_rate = 5

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
    # Do not remove this, current stack used for loading all data to files
    if points is None:
        logging.info(
            "Coord list is empty... Loading cities/villages data on mem...")
        points = load_data()

    while run:
        sleep(1)
        if (abs(datetime.now() - current_date).seconds) >= refresh_rate:
            curr_coords = None
            current_date = datetime.now()
            logging.info("Refreshing GPS data...")
            # curr_coords = get_position_data(gpsd)
            while curr_coords is None:
                curr_coords = get_position_data(gpsd)
                
            print(curr_coords)
        # coord_point = {'lat': initial_coord['lat'], 'lon': initial_coord['lon']}
        # nearest_city = get_nearest_point(points.get('cities'), coord_point)
        # nearest_village = get_nearest_point(points.get('villages'), coord_point)



    # TODO: Move this where neccesary. Currently not used do to while True loop.
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
