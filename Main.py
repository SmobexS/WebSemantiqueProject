from TriplestoreFunctions import *
from rdflib import Namespace
from getJson import *
from JsonToRdf import *
from RdfToSparql import *
from JsonLDScraper import *

file = get_json()

graph = json2rdf(file)

insert_query = generate_insert_query(graph)

print("===================================== TRIPELSTORE DATA =====================================\n")

data = insert_data(insert_query)

visualize_data(data)

print("===================================== JSON-LD =====================================\n")

JsonLD = JsonLDScraper(file)
print (len(JsonLD))

with open('JsonLD.txt', 'w') as file:
    for cop, restos in JsonLD.items():
        for resto, jsonld in restos.items():
            file.write("Coop \" ", cop, "\" :\n")
            file.write("\t Restaurant \" ", resto, "\" :\n")
            file.write("\t\t", jsonld, "\n")
            file.write("==========================================================================\n")