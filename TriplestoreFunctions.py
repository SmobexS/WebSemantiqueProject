from rdflib import ConjunctiveGraph, URIRef, Literal
from SPARQLWrapper import JSON, TURTLE, SPARQLWrapper, POST

fuseki_endpoint_url = 'http://localhost:3030/ProjetWebSementic/'


def import_data (fuseki_endpoint_url) : 

    try:
        triplets = SPARQLWrapper(fuseki_endpoint_url + 'query')
        triplets.setMethod(POST)
        triplets.setReturnFormat(JSON)
        triplets.setQuery("SELECT * WHERE {?sub ?pred ?obj .}")

        # Obtenir les résultats de la requête SPARQL
        sparql_results = triplets.query().convert()

        # Initialiser le graph RDF
        import_result = ConjunctiveGraph()

        # Charger les résultats dans le graph RDF
        for binding in sparql_results['results']['bindings']:
            subject = URIRef(binding['sub']['value'])
            predicate = URIRef(binding['pred']['value'])
            if binding['obj']['type'] == 'uri':
                obj = URIRef(binding['obj']['value'])
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

def delete_data(delete_query):
    
    triplets = SPARQLWrapper(fuseki_endpoint_url + 'update')
    triplets.setMethod(POST)
    triplets.setQuery(delete_query)
    triplets.query()

    return(import_data(fuseki_endpoint_url))

def update_data(update_query):
    
    triplets = SPARQLWrapper(fuseki_endpoint_url + 'update')
    triplets.setMethod(POST)
    triplets.setQuery(update_query)
    triplets.query()

    return(import_data(fuseki_endpoint_url))

def visualize_data (data):
    for row in data:
        print(row)
