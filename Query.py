from RdfToSparql import *
from TriplestoreFunctions import *

from rdflib import Graph, URIRef, Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON

def generate_opening_hours_query(restaurant_uri):
    query = f"""
    PREFIX ns1: <"""+restaurant_uri+""">

    SELECT ?restaurant ?opens ?closes
    WHERE {
      ?restaurant a ns1:Restaurant ;
                  ns1:openingHoursSpecification ?openingHours .

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Monday" ;
                      ns1:opens ?opensMonday ;
                      ns1:closes ?closesMonday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Tuesday" ;
                      ns1:opens ?opensTuesday ;
                      ns1:closes ?closesTuesday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Wednesday" ;
                      ns1:opens ?opensWednesday ;
                      ns1:closes ?closesWednesday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Thursday" ;
                      ns1:opens ?opensThursday ;
                      ns1:closes ?closesThursday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Friday" ;
                      ns1:opens ?opensFriday ;
                      ns1:closes ?closesFriday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Saturday" ;
                      ns1:opens ?opensSaturday ;
                      ns1:closes ?closesSaturday .
      }

      OPTIONAL {
        ?openingHours ns1:dayOfWeek "Sunday" ;
                      ns1:opens ?opensSunday ;
                      ns1:closes ?closesSunday .
      }

      BIND(COALESCE(?opensMonday, ?opensTuesday, ?opensWednesday, ?opensThursday, ?opensFriday, ?opensSaturday, ?opensSunday) AS ?opens)
      BIND(COALESCE(?closesMonday, ?closesTuesday, ?closesWednesday, ?closesThursday, ?closesFriday, ?closesSaturday, ?closesSunday) AS ?closes)
    }
    """

    return query

def execute_sparql_query(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return results['results']['bindings']
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")
        return None

  
def generate_query(restaurant_uris):
    queries = []
    for restaurant_uri in restaurant_uris:
        query = generate_opening_hours_query(restaurant_uri)
        queries.append(query)

    return queries