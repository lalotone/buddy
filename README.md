# Buddy. A live fellow traveler.

# The idea for this project is to create an small service that gives you this info based on GPS data.
# This idea "came alive" when I was with a friend on Dublin for first time and we didn't know where the
# hell to take a meal, pint, etc. The idea is to have this small (but complete) service to provide you all
# the interesting information that is near to you.
- Weather
- Possible sites for (currently opened) ordered by rate:
    - Breakfast
    - Lunch
    - Dinner
    - Beer
- If there is any Tram/Bus/Metro/Train near to you, give you the current info of the different lines.
- Bike parking.f

Extra data:

- Specific feature: Current house consumption and status: Based on Meross/custom sensors implementation.

# APIs that will be consumed:
- OpenWeather for getting the current weather and the next days forecast.
- Google Maps API for getting the different data for breakfast, lunch, dinner and beer.
- ?

# This is a live project, any extra idea will be pushed to the repo as a new feature.

Main hardware:
### Raspberry Pi
### USB GPS
### WiFi AP

Some useful info:
### Formula to obtain the nearest location: https://stackoverflow.com/questions/59736682/find-nearest-location-coordinates-in-land-using-python
### Search for some page like this one to obtain the Cities/Villages DB: https://simplemaps.com/data/world-cities
### Cool site to obtain the current cities/villages: https://overpass-turbo.eu/

TODOs:

- Prepare all the DTOs for public transport. This will be hard and require invest time on different public transport websites/APIs.
- Develop GPS data retrieval from USB.
- Develop all the stack for the Google Near Places API.
- Think of a basic "offline" mode to download all the maps relative to EU countries and obtain all villages and cities... This could be hard too...
- Prepare a "predictable travel" mode where you pass to the Buddy the preferences for the place where you'll go based on keywords. Ex: "sushi, beer, museums, parks" 
