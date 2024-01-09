import threading
from TriplestoreFunctions import *
from JsonToRdf import *
from RdfToSparql import *
from JsonLDScraper import *
from JsonLD2Graph import *


def collect(url='https://coopcycle.org/coopcycle.json?_=1704296951899'):

    graph = import_data()

    if len(graph) == 0:

        new_dataset()

        return None
    
    else:

        thread = threading.Thread(target=update_dataset)
        
        return thread

        

def new_dataset (url='https://coopcycle.org/coopcycle.json?_=1704296951899'):

    graph = json2rdf(url)
    json_ld = JsonLDScraper(url)
    graph = jsonld_to_graph(json_ld, graph)

    insert_query = generate_insert_query(graph)
    graph = insert_data(insert_query)

    graph = graph.serialize(destination="combined_rdf.txt" ,format='turtle')

def update_dataset (url='https://coopcycle.org/coopcycle.json?_=1704296951899'):

    graph = json2rdf(url)
    json_ld = JsonLDScraper(url)
    graph = jsonld_to_graph(json_ld, graph)
        
    insert_query = generate_insert_query(graph)

    delete_data()

    graph = insert_data(insert_query)

    graph = graph.serialize(destination="combined_rdf.txt" ,format='turtle')

    