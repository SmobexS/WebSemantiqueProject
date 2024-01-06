from rdflib import ConjunctiveGraph, Namespace

SCHEMA = Namespace('http://schema.org/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

def jsonld_to_graph(jsonld_data):
    graph = ConjunctiveGraph()
    graph.parse(data=jsonld_data, format='json-ld')

    return graph