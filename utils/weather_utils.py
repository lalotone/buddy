import requests
import logging
# Sample response with NOT OK code: {"cod":"404","message":"city not found"}
# Sample response with OK code:
"""
{
   "coord":{
      "lon":-0.1257,
      "lat":51.5085
   },
   "weather":[
      {
         "id":803,
         "main":"Clouds",
         "description":"broken clouds",
         "icon":"04n"
      }
   ],
   "base":"stations",
   "main":{
      "temp":278.43,
      "feels_like":277.07,
      "temp_min":276.87,
      "temp_max":279.65,
      "pressure":1006,
      "humidity":85
   },
   "visibility":10000,
   "wind":{
      "speed":1.79,
      "deg":282,
      "gust":5.36
   },
   "clouds":{
      "all":72
   },
   "dt":1638814707,
   "sys":{
      "type":2,
      "id":2019646,
      "country":"GB",
      "sunrise":1638777042,
      "sunset":1638805968
   },
   "timezone":0,
   "id":2643743,
   "name":"London",
   "cod":200
}
"""


def get_weather_by_location(location, country, api_key):
    logging.info(f"Getting weather for location: {location}")
    final_url = f"https://api.openweathermap.org/data/2.5/weather?q={location},{country}&APPID={api_key}&units=metric"
    try:
        resp = requests.get(final_url).json()
        if resp.get('cod') == 404:
            logging.error(f"Weather info not found for location: {location}")
            return None
        elif resp.get('cod') == 200:
            logging.info(f"Weather info found for location: {location}")
            return resp
        else:
            logging.error(f"Error obtaining weather for: {location}")
            return None
    except exception:
        print(exception)


def get_weather(weather_api_key, locations, location_country="es"):
    # TODO: Unpack here the locations for the village and the city
    if None in [locations.get('city'), locations.get('village')]:
        return None

    if locations.get('city').get('distance') > locations.get('village').get(
            'distance'):
        selected_location = locations.get('village').get('name')
    else:
        selected_location = locations.get('city').get('name')

    return get_weather_by_location(api_key=weather_api_key,
                                   location=selected_location,
                                   country=location_country)
