from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *
from DataToTable import * 

"""
Main class for query generator and executor

"""
def visualize_data(nbr_resultat, table):
    visualize_table(nbr_resultat, table)

def get_date_time():
  dates = get_date_from_user()
  day = dates[0]
  date_string = dates[1]
  time_filter = get_time_from_user(date_string)
  return day,time


def get_location_criteria():
    print("Choose how to search for restaurants:")
    print("1. By latitude and longitude")
    print("2. By distance from a place")
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        latitude = input("Enter latitude: ")
        longitude = input("Enter longitude: ")
        return {"latitude": latitude, "longitude": longitude}
    elif choice == "2":
        place = input("Enter the name of the place: ")
        max_distance = input("Enter maximum distance in kilometers: ")
        return {"place": place, "max_distance": max_distance}
    else:
        print("Invalid choice. Please choose 1 or 2.")
        return get_location_criteria()

   
# First query that looks for restaurants that are open at a given date and time 
def get_open_restaurants():
  day, time = get_date_time()
  search_query = generate_search_query(day, time)
  data = search_data(search_query)
  table = data_table(data)
  nbr_resultat = len(table.rows)
  visualize_data(nbr_resultat,table)
  return table, nbr_resultat


# Second query to get restaurants in a particular zone or at a maximum distance from some location.
def get_restaurants_by_place():
    day, time = get_date_time()
    location_criteria = get_location_criteria()
    search_query = search_by_place(day, time, **location_criteria)
    data = search_data(search_query)
    table = data_table(data)
    nbr_resultat = len(table.rows)
    visualize_data(nbr_resultat, table)

def main():
    print("Choose an option:")
    print("1. Get open restaurants at a specific date and time")
    print("2. Get restaurants by location criteria")
    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        get_open_restaurants()
    elif choice == "2":
        get_restaurants_by_place()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()