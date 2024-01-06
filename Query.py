from rdfToSparql import *
from triplestoreFunctions import *
from Date_time import *
from DataToTable import *
import argparse 
from rdflib import Graph, Namespace, URIRef, Literal

class Query:
    def __init__(self):
        self.tripleStore = TripleStore()
        self.rdfToSparql = RdfToSparQL()
    
    def get_date_time(self):
        dates = get_date_from_user()
        day = dates[0]
        date_string = dates[1]
        time_filter = get_time_from_user(date_string)
        return day,time_filter

    def visualize(self,search_query):
        data = self.tripleStore.search_data(search_query)
        table = data_table(data)
        nbr_resultat = len(table.rows)
        visualize_table(nbr_resultat, table)

    def get_location_criteria(self):
        print("Choose how to search for restaurants:")
        print("1. By city")
        print("2. By latitude and longitude")
        print("3. By distance from a place")
        choice = input("Enter your choice (1 or 2 or 3): ")
        if choice == "1":
            city = input("Enter city: ")
            city = unicodeTostr(city)
            max_distance = 0
            return {"type":"city" ,"coordinates": city, "max_distance": max_distance}
        elif choice == "2":
            latitude = input("Enter latitude: ")
            longitude = input("Enter longitude: ")
            max_distance = input("Enter maximum distance in kilometers: ")
            return {"type":"geocord" ,"coordinates": (latitude, longitude), "max_distance": max_distance}
        elif choice == "3":
            place = input("Enter the name of the place: ")
            max_distance = input("Enter maximum distance in kilometers: ")
            return {"type":"address" ,"coordinates": place, "max_distance": max_distance}
        else:
            print("Invalid choice. Please choose 1 or 2.")
            return self.get_location_criteria()

    
    # First query that looks for restaurants that are open at a gget_location_criteriaget_restaurants_by_placeiven date and time 
    def get_open_restaurants(self):
        day, time = self.get_date_time()
        search_query = self.rdfToSparql.generate_search_query(day, time)
        self.visualize(search_query)
        return search_query


    # Second query to get restaurants in a particular zone or at a maximum distance from some location.
    def get_restaurants_by_place(self,day, time, coordinates, max_distance):
        location_criteria = self.get_location_criteria() 
        print(location_criteria['type'])
        search_query =  self.rdfToSparql.get_by_place(day, time,location_criteria['type'] , coordinates, max_distance)
        self.visualize(search_query)
        return search_query

    #Third query to get restaurants accepting delivery below a certain price.
    def get_restaurants_by_max_delivery_price(self,day, time, max_price):
        search_query =  self.rdfToSparql.get_by_max_price(day, time,max_price)
        self.visualize(search_query)
        return search_query


    #Fourth query to rank restaurants by distance or minimum delivery price 
    def get_restaurants_by_ranking(self,day, time, coordinates, max_distance, rank_by, max_price=None):
        if rank_by == "distance":
            search_query = self.get_restaurants_by_place(day, time, coordinates, max_distance)
            print("louwel---------")
            print(search_query)
            print("louwel----------")
        elif rank_by == "price":
            search_query = self.get_restaurants_by_max_delivery_price(day, time, max_price)
            print("tani------")
            print(search_query)
            print("tani------")
        else:
            print("Invalid ranking option. Please choose 'distance' or 'price'.")
            return
        self.visualize(search_query)



    #Get the preferences from the file pref-charpenay.ttl
    def get_user_preferences(self,uri):
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

