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

visualize_table(nbr_resultat, table)

