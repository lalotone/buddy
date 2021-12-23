from dataclasses import dataclass
import json
import logging
import geopy.distance

# Awesome, from: https://stackoverflow.com/questions/59736682/find-nearest-location-coordinates-in-land-using-python
# Implementation on the response:
"""
# city = {'lat_key': value, 'lon_key': value}  # type:dict()
new_york = {'lat': 40.712776, 'lon': -74.005974}
washington = {'lat': 47.751076,  'lon': -120.740135}
san_francisco = {'lat': 37.774929, 'lon': -122.419418}

city_list = [new_york, washington, san_francisco]

city_to_find = {'lat': 29.760427, 'lon': -95.369804}  # Houston
print(find_closest_lat_lon(city_list, city_to_find))
"""


@dataclass
class Point:
    name: str
    typeof: str
    coords: dict


"""
Only the relevant parts from the JSON that will be used.
{
  "properties": {
    "name": "Alacant / Alicante",
    "place": "city"
  },
  "geometry": {
    "coordinates": [
      -0.4881708,
      38.3436365
    ]
  }
}
"""


def get_position_data(gps):
    nx = gps.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    logging.info("Trying to obtain position from GPS...")
    if nx['class'] == 'TPV':
        if getattr(nx, 'lat') is not None and getattr(nx, 'lon') is not None:
            latitude = float(getattr(nx, 'lat'))
            longitude = float(getattr(nx, 'lon'))
            logging.info(f"Your position: lon = {longitude} lat = {latitude}")
            return {"lat": latitude, "lon": longitude}

        logging.error("Unknown lon/lat. Ignoring the coord point")

    return None


def initialize_data():
    # try:
    villages_list = []
    cities_list = []
    with open('./utils/villages.geojson') as village_data:
        villages = village_data.read()

    with open('./utils/cities.geojson') as cities_data:
        cities = cities_data.read()

    if cities is not None:
        cities_json = json.loads(cities)['features']
        for city in cities_json:
            cities_list.append(
                Point(name=city['properties']['name'],
                      typeof=city['properties']['place'],
                      coords={
                          'lat': city['geometry']['coordinates'][1],
                          'lon': city['geometry']['coordinates'][0]
                      }))

    if villages is not None:
        villages_json = json.loads(villages)['features']
        for village in villages_json:
            # print(village.get('name'))
            if village.get('properties', {}).get('name'):
                villages_list.append(
                    Point(name=village['properties']['name'],
                          typeof=village['properties']['place'],
                          coords={
                              'lat': village['geometry']['coordinates'][1],
                              'lon': village['geometry']['coordinates'][0]
                          }))

    if not None in (villages_list, cities_list):
        points_dict = {"cities": cities_list, "villages": villages_list}

    if points_dict != None:
        return points_dict

    return None
    # TODO: Improve this except with better exception handling.
    # except KeyError:
    #     return None
    # except FileNotFoundError:
    #     return None
    # except:
    #     return None


def dist_between_two_lat_lon(*args):
    from math import asin, cos, radians, sin, sqrt
    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats = abs(lat2 - lat1)
    dist_longs = abs(long2 - long1)
    a = sin(dist_lats / 2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs / 2)**2
    c = asin(sqrt(a)) * 2
    radius_earth = 6378  # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    return c * radius_earth


def find_closest_lat_lon(data, v):
    try:
        return min(data,
                   key=lambda p: dist_between_two_lat_lon(
                       v['lat'], p['lat'], v['lon'], p['lon']))
    except TypeError:
        logging.error('Not a list or not a number.')


def get_nearest_point(points, testing_point):
    for point in points:
        coords_list = [point.coords for point in points]

    if coords_list != None:
        logging.info(
            f"Obtaining nearest location to lat: {testing_point['lat']} lon: {testing_point['lon']}"
        )

        found_coords = find_closest_lat_lon(coords_list, testing_point)
        for point in points:
            if found_coords == point.coords:
                logging.info(
                    "Getting distance between GPS data and nearest village/city."
                )
                distance = geopy.distance.distance(
                    (testing_point["lat"], testing_point["lon"]),
                    (point.coords["lat"], point.coords["lon"])).km
                logging.info(
                    f"Nearest location: {point.name}. Type: {point.typeof}. Distance between points: {distance} Km"
                )
                return {"name": point.name, "distance": distance}

    return None
