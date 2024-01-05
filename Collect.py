from TriplestoreFunctions import *
from getJson import *
from JsonToRdf import *
from RdfToSparql import *
from JsonLDScraper import *
from JsonLD2Graph import *

delete_data()

file = get_json()
graph = json2rdf(file)
insert_query = generate_insert_query(graph)
data = insert_data(insert_query)
json_ld = JsonLDScraper(file)
data_comb = ConjunctiveGraph()
for cop, restos in json_ld.items():
    for resto, jsonld in restos.items():
        graph_jld = jsonld_to_graph(jsonld)
        graph_jld.add((URIRef(cop), pwsp.CanDeliverFoodOf, URIRef(resto)))
        insert_query = generate_insert_query(graph_jld)
        data_comb = insert_data(insert_query)

data_comb = data_comb.serialize(destination="combined_rdf.txt" ,format='turtle')



