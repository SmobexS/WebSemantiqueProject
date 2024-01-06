import requests
from geopy.geocoders import *
from geopy.distance import geodesic
from geopy.exc import *

def get_coordinates(place):
    geolocator = Nominatim(user_agent="WebSemantiqueProject")
    location = geolocator.geocode(place, language='en')
    return location.latitude, location.longitude
    
    
def validate_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="WebSemantiqueProject")

    try:
        location = geolocator.reverse((latitude, longitude), language='en')
        print(f"Valid Coordinates: {location.address}")
        return True
    except GeocoderQueryError as e:
        print(f"Invalid Coordinates: {e}")
        return False
    
def valid_place(place):
    geolocator = Nominatim(user_agent="WebSemantiqueProject")

    try:
        location = geolocator.geocode(place, language='en')
        print(f"Valid Place: {location.address}")
        return True
    except GeocoderQueryError as e:
        print(f"Invalid Place: {e}")
        return False
    
def find_restaurent_within_max_distance(data, coordinates, max_distance):
    if len(data["results"]["bindings"]) == 0:
        return (data, 0)
    else:
        result = {"head":dict(), "results":{"bindings":[]}}
        result["head"]["vars"] = ["restaurant", "name", "openingTime", "closingTime", "address", "distance from your location(m)"]
        for binding in data["results"]["bindings"]:
            if within_max_distance(binding["latitude"]["value"], binding["longitude"]["value"], coordinates, max_distance):
                bind = dict()
                bind["restaurant"] = binding["restaurant"]
                bind["name"] = binding["name"]
                bind["openingTime"] = binding["openingTime"]
                bind["closingTime"] = binding["closingTime"]
                bind["address"] = binding["address"]
                bind["distance from your location(m)"] = {"value":get_distance_between_coordinates(coordinates, (binding["latitude"]["value"], binding["longitude"]["value"]))*1000}
                result["results"]["bindings"].append(bind)

        if len(result["results"]["bindings"]) == 0:
            return (result, 1)
        else:
            return (result, 2)
        
def within_max_distance(latitude, longitude, coordinates, max_distance):
    distance = get_distance_between_coordinates(coordinates, (latitude, longitude))
    if distance <= max_distance:
        return True
    else:
        return False

def get_distance_between_coordinates(coordinates1, coordinates2):
    distance_km = geodesic(coordinates1, coordinates2).kilometers
    return float(distance_km)