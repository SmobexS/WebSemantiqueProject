from rdflib import ConjunctiveGraph, Namespace, URIRef

pwsp = Namespace("https://ProjectW9s.com/predicate/")

def jsonld_to_graph(jsonld_data, graph):

    data_comb = ConjunctiveGraph()
    jsonld_graph = ConjunctiveGraph()

    for cop, restos in jsonld_data.items():
        for resto, jsonld in restos.items():

            temp_graph = ConjunctiveGraph()

            temp_graph.parse(data=jsonld, format='json-ld')
            temp_graph.add((URIRef(cop), pwsp.CanDeliverFoodOf, URIRef(resto)))

            jsonld_graph += temp_graph

    data_comb += graph
    data_comb += jsonld_graph


    return data_comb
