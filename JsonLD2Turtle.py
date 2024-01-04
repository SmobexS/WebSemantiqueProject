from rdflib import Graph, Namespace
from JsonLDScraper import *

graph = Graph()

SCHEMA = Namespace('http://schema.org/')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

def jsonld_to_rdf(jsonld_data):
    graph = ConjunctiveGraph()
    graph.parse(data=jsonld_data, format='json-ld')
    return graph
