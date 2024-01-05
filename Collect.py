from TriplestoreFunctions import *
from getJson import *
from JsonToRdf import *
from RdfToSparql import *
from JsonLDScraper import *
from JsonLD2Turtle import *
from Query import *

delete_data()

file = get_json()
graph = json2rdf(file)
insert_query = generate_insert_query(graph)
data = insert_data(insert_query)
json_ld = JsonLDScraper(file)
data_comb = ConjunctiveGraph()
for cop, restos in json_ld.items():
    for resto, jsonld in restos.items():
        graph_jld = jsonld_to_turtle(jsonld)
        graph_jld.add((URIRef(cop), pwsp.CanDeliverFoodOf, URIRef(resto)))
        insert_query = generate_insert_query(graph_jld)
        data_comb = insert_data(insert_query)

# Opening hours query :
restaurant_uris = [resto_uri for cop, restos in json_ld.items() for resto_uri in restos.keys()]
queries = generate_query(restaurant_uris)
endpoint_url = 'http://localhost:3030/ProjetWebSementic'

for query in queries:
    result = execute_sparql_query(endpoint_url, query)
    print(f"Results for query: {query}")
    print(result)


data_comb = data_comb.serialize(destination="combined_rdf.txt" ,format='turtle')



