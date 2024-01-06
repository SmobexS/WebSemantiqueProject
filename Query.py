from RdfToSparql import *
from TriplestoreFunctions import *
from Date_time import *
from DataToTable import * 

dates = get_date_from_user()
day = dates[0]
date_string = dates[1]
time_filter = get_time_from_user(date_string)

search_query = generate_search_query(day, time_filter)
data = search_data(search_query)

table = data_table(data)

nbr_resultat = len(table.rows)

if nbr_resultat == 0:
    print("No restaurant is open at this time. Try an other time.")
else:
    print(f"{nbr_resultat} restaurants are open at this time.")
    valide = False

    nb = input("How many restaurants do you want to see ? (All by default if you press Enter) : ") or nbr_resultat
    
    min = 0

    while valide == False:
        nb = int(nb)
        if nb >= nbr_resultat:
            nb = nbr_resultat
            valide = True

        table_print = table[min:nb+1]

        print(table_print)

        if nb < nbr_resultat:
            d = input("Do you want to see more restaurants ? (y/n) : ")
            if d.lower() == "y":
                min = nb + 1
                nb += 10
            else:
                valide = True

