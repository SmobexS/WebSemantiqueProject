from jsonLDScrapper import *
from jsonToRDF import *
from triplestoreFunctions import *
from getJson import *
from rdfToSparql import *
from query import *

jsonToRDF = JsonToRDF()
tripleStore = TripleStore()
jsontLDScrapper = JsonLDScraper()
rdfToSparQL = RdfToSparQL()

tripleStore.delete_data()

file = get_json()
graph = jsonToRDF.transform(file)
insert_query = rdfToSparQL.generate_insert_query(graph)
data = tripleStore.insert_data(insert_query)

json_ld = jsontLDScrapper.scrapper(file)

data_comb = ConjunctiveGraph()
for cop, restos in json_ld.items():
    for resto, jsonld in restos.items():
        graph_jld = jsontLDScrapper.graph(jsonld)
        graph_jld.add((URIRef(cop), pwsp.CanDeliverFoodOf, URIRef(resto)))
        insert_query = rdfToSparQL.generate_insert_query(graph_jld)
        data_comb = tripleStore.insert_data(insert_query)
data_comb = data_comb.serialize(destination="combined_rdf.txt" ,format='turtle')



