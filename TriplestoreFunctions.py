from rdflib import ConjunctiveGraph, URIRef, Literal, BNode
from SPARQLWrapper import JSON, SPARQLWrapper, POST

fuseki_endpoint_url = 'http://localhost:3030/ProjetWebSementic/'

def import_data (fuseki_endpoint_url='http://localhost:3030/ProjetWebSementic/') : 

    try:
        triplets = SPARQLWrapper(fuseki_endpoint_url + 'query')
        triplets.setMethod(POST)
        triplets.setReturnFormat(JSON)
        triplets.setQuery("SELECT * WHERE {?sub ?pred ?obj .}")

        sparql_results = triplets.query().convert()

        import_result = ConjunctiveGraph()

        for binding in sparql_results['results']['bindings']:
            if binding['sub']['type'] == 'uri':
                subject = URIRef(binding['sub']['value'])
            elif binding['sub']['type'] == 'bnode':
                subject = BNode(binding['sub']['value'])
            predicate = URIRef(binding['pred']['value'])
            if binding['obj']['type'] == 'uri':
                obj = URIRef(binding['obj']['value'])
            elif binding['obj']['type'] == 'bnode':
                obj = BNode(binding['obj']['value'])
            elif binding['obj']['type'] == 'literal':
                if binding['obj'].keys().__contains__('xml:lang'):
                    obj = Literal(binding['obj']['value'], lang=binding['obj']['xml:lang'])
                elif binding['obj'].keys().__contains__('datatype'):
                    obj = Literal(binding['obj']['value'], datatype=URIRef(binding['obj']['datatype']))
                else:
                    obj = Literal(binding['obj']['value'])
            import_result.add((subject, predicate, obj))

    except Exception as e:
        print(f"Erreur lors de la connexion au triplestore : {e}")

    return(import_result)

def insert_data(insert_query):

    triplets = SPARQLWrapper(fuseki_endpoint_url + 'update')
    triplets.setMethod(POST)
    triplets.setQuery(insert_query)
    triplets.query()

    return(import_data(fuseki_endpoint_url))

def delete_data():
    
    delete_query = "DELETE WHERE {?sub ?pred ?obj .}"
    
    triplets = SPARQLWrapper(fuseki_endpoint_url + 'update')
    triplets.setMethod(POST)
    triplets.setQuery(delete_query)
    triplets.query()

def visualize_data (data):
    for row in data:
        print(row)
