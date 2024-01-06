from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *

date_filter = get_date_from_user()
time_filter = get_time_from_user()

search_query = generate_search_query(date_filter, time_filter)
data = search_data(search_query)

nbr_resultat = len(data)-1

table = [data["head"]["vars"]]
for binding in data["results"]["bindings"]:
    table.append([binding["restaurant"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"]])

if nbr_resultat == 0:
    print("No restaurant is open at this time. Try an other time.")
else:
    print(f"{nbr_resultat} restaurants are open at this time.")
    nb = input("How many restaurants do you want to see ? (All by default) : ") or nbr_resultat
    nb = int(nb)
    if nb > nbr_resultat:
        nb = nbr_resultat
    
    table_print = table[:nb+1]

    for row in table_print:
        for cell in row:
            print(cell, end='\t')
        print()

