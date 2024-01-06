from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *
from DataToTable import *
from CoordOperations import *

def get_date_time():
  dates = get_date_from_user()
  day = dates[0]
  date_string = dates[1]
  time_filter = get_time_from_user(date_string)
  return day,time_filter


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

   
# First query that looks for restaurants that are open at a given date and time 
def get_open_restaurants():
  day, time = get_date_time()
  search_query = generate_search_query(day, time)
  data = search_data(search_query)
  table = data_table(data)
  nbr_resultat = len(table.rows)
  visualize_table(nbr_resultat,table)


# Second query to get restaurants in a particular zone or at a maximum distance from some location.
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
    get_restaurants_by_place()
    

if __name__ == "__main__":
    main()