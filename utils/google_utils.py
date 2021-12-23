import json


# TODO: Implement the all-call system to download all available data on current
# city/village according to restaurants, pubs, etc. It's like an automatic polling
# using the current nearest location. Here some methods that will implement that
def poll_near_places():
    # Here we'll do a loop with all the typical places that you want to visit.
    # This can be adjusted based on the types of places and keywords that uses
    # the Google's Nearby Search API and Places.
    pass


def parse_data():
    # This method is used to parse all the data that is obtained from Google Places API
    print(
        "Currently debug mode.... remember to change this path to realive (complete) one."
    )
    # First except
    source_data = open('./near_restaurants.json', 'r').read()
    # Second except
    json_data = json.loads(source_data)
    results = json_data.get('results')
    if results is not None:
        for result in results:
            print(result.get('name'))


if __name__ == "__main__":
    parse_data()
