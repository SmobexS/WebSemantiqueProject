from TriplestoreFunctions import *
from rdflib import Namespace
from getJson import *
from JsonToRdf import *
from RdfToSparql import *

file = get_json()

graph = json2rdf(file)

insert_query = generate_insert_query(graph)

data = insert_data(insert_query)

visualize_data(data)