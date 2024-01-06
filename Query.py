from CoordOperations import *
from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *
from DataToTable import *
import argparse 
from rdflib import Graph, Namespace, URIRef, Literal

def get_date_time():
  dates = get_date_from_user()
  day = dates[0]
  date_string = dates[1]
  time_filter = get_time_from_user(date_string)
  return day,time_filter

def visualize(search_query):
    data = search_data(search_query)
    table = data_table(data)
    nbr_resultat = len(table.rows)
    visualize_table(nbr_resultat, table)

def get_location_criteria():
    print("Choose how to search for restaurants:")
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
            return {"type":"city" ,"coordinates": list_of_cities[city-1]}
        else :
            print("Invalid city. Please try again.")
            return get_location_criteria()
    elif choice == "2":
        latitude = input("Enter latitude: ")
        longitude = input("Enter longitude: ")
        if validate_coordinates(latitude, longitude):
            max_distance = float(input("Enter maximum distance in kilometers: "))
        else :
            print("Invalid coordinates. Please try again.")
            return get_location_criteria()
        return {"type":"geocord" ,"coordinates": (latitude, longitude), "max_distance": max_distance}
    elif choice == "3":
        place = input("Enter the name of the place: ")
        if valid_place(place):
            max_distance = float(input("Enter maximum distance in kilometers: "))
        else :
            print("Invalid place. Please try again.")
            return get_location_criteria()
        return {"type":"address" ,"coordinates": get_coordinates(place), "max_distance": max_distance}
    else:
        print("Invalid choice. Please choose 1 or 2 or 3.")
        return get_location_criteria()

   
# First query that looks for restaurants that are open at a gget_location_criteriaget_restaurants_by_placeiven date and time 
def get_open_restaurants():
  day, time = get_date_time()
  search_query = generate_search_query(day, time)
  visualize(search_query)
  return search_query


# Second query to get restaurants in a particular zone or at a maximum distance from some location.
#def get_restaurants_by_place(day, time, coordinates, max_distance):
#   location_criteria = get_location_criteria() 
#    print(location_criteria['type'])
#    search_query = get_restaurants_by_place(day, time,location_criteria['type'] , coordinates, max_distance)
#    visualize(search_query)
#    return search_query

#Third query to get restaurants accepting delivery below a certain price.
def get_restaurants_by_max_delivery_price(day, time, max_price):
    search_query = get_by_max_price(day, time,max_price)
    visualize(search_query)
    return search_query


#Fourth query to rank restaurants by distance or minimum delivery price 
def get_restaurants_by_ranking(day, time, coordinates, max_distance, rank_by, max_price=None):
    if rank_by == "distance":
        search_query = get_restaurants_by_place(day, time, coordinates, max_distance)
        print("louwel---------")
        print(search_query)
        print("louwel----------")
    elif rank_by == "price":
        search_query = get_restaurants_by_max_delivery_price(day, time, max_price)
        print("tani------")
        print(search_query)
        print("tani------")
    else:
        print("Invalid ranking option. Please choose 'distance' or 'price'.")
        return
    visualize(search_query)



#Get the preferences from the file pref-charpenay.ttl
def get_user_preferences(uri):
    g = Graph()
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

         
def get_restaurants_by_place():
    day, time = get_date_time()
    location_criteria = get_location_criteria()
    search_query = search_by_place(day, time, location_criteria["type"], location_criteria["coordinates"])
    data = search_data(search_query)
    if location_criteria["type"] == "city":
        if len(data["results"]["bindings"]) == 0:
            result = (data, 0)
        else:
            result = (data, 2)
    else:
        result = find_restaurent_within_max_distance(data, location_criteria["coordinates"], location_criteria["max_distance"])
    table = data_table(result[0], location_criteria["type"])
    nbr_resultat = len(table.rows)
    visualize_table(nbr_resultat, result[1], table)


def main():
    parser = argparse.ArgumentParser(description="CoopCycle restaurants query program:")
    parser.add_argument("--rank-by", choices=["distance", "price"], help="Ranking restaurants by distance or price")
    parser.add_argument("--user-preferences", action="store_true", help="User preferences from .ttl file")
    args = parser.parse_args()

    if args.user_preferences:
        pref_uri = "https://www.emse.fr/~zimmermann/Teaching/SemWeb/Project/pref-charpenay.ttl"
        user_preferences = get_user_preferences(pref_uri)

        if 'seller' in user_preferences:
            print("User is looking for restaurants near:", user_preferences.get('location', "Not specified"))
            print("User is looking for restaurants from seller:", user_preferences['seller'])
            print("User has a maximum budget of", user_preferences['max_price'][0], user_preferences['max_price'][1])

            if args.rank_by in ["distance", "price"]:
                day, time = get_date_time()

                if 'location' in user_preferences:
                    coordinates = user_preferences['location'][:2]
                    max_distance = user_preferences['location'][2]
                else:
                    coordinates = None
                    max_distance = None

                if args.rank_by == "distance":
                    get_restaurants_by_ranking(day, time, coordinates, max_distance, "distance")
                elif args.rank_by == "price" and 'max_price' in user_preferences:
                    max_price = user_preferences['max_price'][0]
                    get_restaurants_by_ranking(day, time, coordinates, max_distance, "price", max_price)
                else:
                    print("Invalid ranking option or user preferences. Please check your input.")
            else:
                print("Invalid ranking option. Please choose 'distance' or 'price'.")
        else:
            print("Seller information not found in user preferences.")
    else:
        if args.rank_by:
            print("Error: When using --rank-by, --user-preferences is required.")
        else:
            print("Error: --rank-by option is required.")

   


if __name__ == "__main__":
    main()
