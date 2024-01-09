from urllib.parse import urlparse
from CoordOperations import *
from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *
from DataToTable import *
import argparse 
from rdflib import Graph, Namespace, URIRef

def get_date_time():
  dates = get_date_from_user()
  day = dates[0]
  date_string = dates[1]
  time_filter = get_time_from_user(date_string)
  return day,time_filter

def visualize(data, type, code_err = 2):
    table = data_table(data, type)
    nbr_resultat = len(table.rows)
    visualize_table(nbr_resultat, code_err, table)

def get_location_criteria():
    print("Choose how to search for restaurants :")
    print("1. By city")
    print("2. By latitude and longitude")
    print("3. By distance from a place")
    choice = input("Enter your choice (1 or 2 or 3): ")
    if choice == "1":
        list_of_cities = get_list_of_cities()
        print("List of cities:\n")
        for i in range(len(list_of_cities)):
            print(f"{i+1}. {list_of_cities[i]}")
        city = int(input("choose a city (1 or 2 etc.): "))
        if city > 0 and city <= len(list_of_cities):
            return {"type":"city" ,"coordinates": list_of_cities[city-1],"max_distance":10}
        else :
            print("Invalid city. Please try again.")
            return get_location_criteria()
    elif choice == "2":
        latitude = input("Enter latitude: ")
        longitude = input("Enter longitude: ")
        if validate_coordinates(latitude, longitude):
            max_distance = input("Enter maximum distance in kilometers (5Km by default if you press Enter): ") or 5
            max_distance = float(max_distance)
        else :
            print("Invalid coordinates. Please try again.")
            return get_location_criteria()
        return {"type":"geocord" ,"coordinates": (latitude, longitude), "max_distance": max_distance}
    elif choice == "3":
        place = input("Enter the name of the place: ")
        if valid_place(place):
            max_distance = input("Enter maximum distance in kilometers (5Km by default if you press Enter): ") or 5
            max_distance = float(max_distance)
        else :
            print("Invalid place. Please try again.")
            return get_location_criteria()
        return {"type":"address" ,"coordinates": get_coordinates(place), "max_distance": max_distance}
    else:
        print("Invalid choice. Please choose 1 or 2 or 3 or press Enter.")
        return get_location_criteria()

#First query to get restaurants by city or geocordinates or address
def get_restaurants_by_place(day, time, location, max_distance, arg = None):
    if arg == None:
        location_criteria = get_location_criteria()
        max_distance = location_criteria["max_distance"]
    else:
        location_criteria = location

    search_query = search_by_place(day, time, location_criteria["type"], location_criteria["coordinates"])
    data = search_data(search_query)
    if location_criteria["type"] == "city":
        if len(data["results"]["bindings"]) == 0:
            result = (data, 0)
        else:
            result = (data, 2)
    else:
        result = find_restaurent_within_max_distance(data, location_criteria["coordinates"], max_distance, "distance")
    
    visualize(result[0], location_criteria['type'], result[1])

    return result, location_criteria['type']

#Seconf query to get restaurants accepting delivery below a certain price.
def get_restaurants_by_max_delivery_price(day, time, coordinates, max_distance, max_price, arg = None):

    if arg == None:
        location_criteria = get_location_criteria()
        type = location_criteria["type"]
        if type == "city":
            coordinates = get_coordinates(location_criteria["coordinates"])
            max_distance = 10
        else:
            coordinates = location_criteria["coordinates"]
            max_distance = location_criteria["max_distance"]
    else:
        coordinates = coordinates
        max_distance = max_distance
        type = "geocord"

    search_query = get_by_max_price(day, time, max_price)
    data = search_data(search_query)
    data = find_restaurent_within_max_distance(data, coordinates, max_distance, "price")
    visualize(data[0], "price", data[1])

#Tird query to rank restaurants by distance or minimum delivery price 
def get_restaurants_by_ranking(day, time, coordinates, max_distance, rank_by, max_price=None, arg = None):
    if rank_by == "distance":
        print("Ranking restaurants by distance...")
        get_restaurants_by_place(day, time, coordinates, max_distance, arg)
       
    elif rank_by == "price":
        print("Ranking restaurants by minimum delivery price...")
        get_restaurants_by_max_delivery_price(day, time, coordinates, max_distance, max_price, arg)
      
    else:
        print("Invalid ranking option. Please choose 'distance' or 'price'.")
        return

#Get the preferences from the file pref-charpenay.ttl
def get_user_preferences(uri):
    g = Graph()
    parsed_url = urlparse(uri)
    if parsed_url.scheme and parsed_url.netloc:
            g.parse(uri, format="turtle")
    elif parsed_url.scheme == '' and parsed_url.netloc == '' and parsed_url.path:
        with open(uri, 'r') as file:
            g.parse(file, format="turtle")
    elif isinstance(uri,Graph):
        g=uri
    else:
        print("Invalid input. Please provide a graph, URL or an RDF file")
    g.parse(uri, format="turtle")
    user_preferences = {}
    schema = Namespace("http://schema.org/")
    print("Number of triples in the graph:", len(g))
    for subj, pred, objet in g:
        if pred == schema.seeks:
            if isinstance(objet, BNode):
                seller = g.value(subject=objet, predicate=schema.seller)
                if seller:
                    user_preferences['seller'] = URIRef(str(seller))
        elif pred == schema.priceSpecification:
            max_price = float(g.value(subject=objet, predicate=schema.maxPrice))
            currency = str(g.value(subject=objet, predicate=schema.priceCurrency))
            user_preferences['max_price'] = (max_price, currency)
        elif pred == schema.availableAtOrFrom:
            location = g.value(subject=objet, predicate=schema.geoWithin)
            if location:
                latitude = float(g.value(subject=location, predicate=schema.geoMidpoint/schema.latitude))
                longitude = float(g.value(subject=location, predicate=schema.geoMidpoint/schema.longitude))
                radius = float(g.value(subject=location, predicate=schema.geoRadius))
                user_preferences['location'] = (latitude, longitude, radius)

    print(" User preferences :::--->", user_preferences)
    return user_preferences





def main(rank_by, uri):
    parser = argparse.ArgumentParser(description="CoopCycle restaurants query program:")
    #parser.add_argument("--rank-by", choices=["distance", "price"], help="Ranking restaurants by distance or price")
    #parser.add_argument("--user-preferences",  help="User preferences from an RDF file")
    #parser.add_argument("--manual-location", action="store_true", help="Input manual location")
    #args = parser.parse_args()

    if uri != None:  
        user_preferences = get_user_preferences(uri)
        #pref_uri = "https://www.emse.fr/~zimmermann/Teaching/SemWeb/Project/pref-charpenay.ttl"
        if 'seller' in user_preferences:
            print("User is looking for restaurants near:", user_preferences.get('location', "Not specified"))
            print("User is looking for restaurants from seller:", user_preferences['seller'])
            print("User has a maximum budget of", user_preferences['max_price'][0], user_preferences['max_price'][1])

            print(rank_by)
            day, time = get_date_time()
            
            if 'location' in user_preferences:
                if validate_coordinates(user_preferences["location"][:2][0], user_preferences["location"][:2][1]) :
                    coordinates = user_preferences['location'][:2]
                    max_distance = user_preferences['location'][2]
                else :
                    coordinates = None
                    max_distance = None
            else:
                coordinates = None
                max_distance = None
            location = {}
            location['type'] = "geocord"
            location['coordinates'] = coordinates
            if rank_by == "distance":
                get_restaurants_by_ranking(day, time, location, max_distance, "distance", arg = 1)
            elif rank_by == "price" and 'max_price' in user_preferences:
                max_price = user_preferences['max_price'][0]
                get_restaurants_by_ranking(day, time, coordinates, max_distance, "price", max_price, arg = 1)
            else:
                print("Invalid ranking option or user preferences. Please check your input.")
        else:
            print("Seller not in user")
    else:
        print("Invalid URI, please enter a URL or a Turtle file location")
    


if __name__ == "__main__":
    main()
