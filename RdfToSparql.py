from rdflib import URIRef, Literal, BNode
from TriplestoreFunctions import search_data
from UnicodeToStr import *

def format_term(term):
    if isinstance(term, URIRef):
        return f"<{term}>"
    elif isinstance(term, BNode):
        return f"_:b{term}"
    elif isinstance(term, Literal):
        if term.language:
            return f'"{term}"@{term.language}'
        elif term.datatype:
            return f'"{term}"^^<{term.datatype}>'
        else:

            term = unicodeTostr(term)
            
            term = term.replace("\n", "")
            term = term.replace("\r", "")
            term = term.replace("\t", "")
            term = term.replace("\\", "")
            
            return f'"{term}"'

def generate_insert_query(graph):
    insert_query = "INSERT DATA {\n"

    for subj, pred, obj in graph:
        subject = format_term(subj)
        predicate = format_term(pred)
        obj = format_term(obj)

        insert_query += f"  {subject} {predicate} {obj} .\n"

    insert_query += "}"

    return insert_query

def generate_search_query(date, time):
    search_query = "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
    search_query += "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
    search_query += "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
    search_query += "PREFIX pwp:<https://ProjectW9s.com/predicate/>\n"
    search_query += "PREFIX pwo:<https://ProjectW9s.com/object/>\n"
    search_query += "PREFIX pws:<https://ProjectW9s.com/subject/>\n"
    search_query += "PREFIX schema: <http://schema.org/>\n"
    search_query += "SELECT ?restaurant ?name ?openingTime ?closingTime ?address\n"
    search_query += "WHERE {\n"
    search_query += "?restaurant a schema:Restaurant ;\n"
    search_query += "schema:name ?name;\n"
    search_query += "schema:address ?address_link;\n"
    search_query += "schema:openingHoursSpecification [\n"
    search_query += "schema:opens ?openingTime ;\n"
    search_query += "schema:closes ?closingTime ;\n"
    search_query += "schema:dayOfWeek ?dayOfWeek\n"
    search_query += "] .\n"
    search_query += "?address_link a schema:PostalAddress;\n"
    search_query += "schema:streetAddress ?address.\n"
  
    search_query += f"FILTER (?dayOfWeek = \"{date}\" && ?openingTime <= \"{time}\" && ?closingTime > \"{time}\")\n"
    search_query += "}\n"

    return search_query

def get_list_of_cities():
    list_of_cities = []
    search_query = (
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
        "PREFIX pwp:<https://ProjectW9s.com/predicate/>\n"
        "PREFIX pwo:<https://ProjectW9s.com/object/>\n"
        "PREFIX pws:<https://ProjectW9s.com/subject/>\n"
        "PREFIX schema: <http://schema.org/>\n"
        "SELECT DISTINCT ?city\n"
        "WHERE {\n"
        "?cooplink pwp:city ?city.\n"
        "}\n"
        "ORDER BY ?city\n"
    )
    data = search_data(search_query)
    for binding in data["results"]["bindings"]:
        list_of_cities.append(binding["city"]["value"])
    return list_of_cities

def search_by_place(day, time, type, coordinates):
    search_query = (
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
        "PREFIX pwp:<https://ProjectW9s.com/predicate/>\n"
        "PREFIX pwo:<https://ProjectW9s.com/object/>\n"
        "PREFIX pws:<https://ProjectW9s.com/subject/>\n"
        "PREFIX schema: <http://schema.org/>\n"
        "PREFIX geof: <http://www.opengis.net/ont/geosparql#>\n"
        "prefix unit: <http://qudt.org/vocab/unit#>\n"
        
    )

    if type == "address" or type == "geocord":
        search_query += (
            "SELECT ?restaurant ?name ?openingTime ?closingTime ?address ?latitude ?longitude\n"
            "WHERE {\n"
            "?restaurant a schema:Restaurant ;\n"
            "schema:name ?name;\n"
            "schema:address ?address_link;\n"
            "schema:openingHoursSpecification [\n"
            "schema:opens ?openingTime ;\n"
            "schema:closes ?closingTime ;\n"
            "schema:dayOfWeek ?dayOfWeek\n"
            "] .\n"
            "?address_link a schema:PostalAddress;\n"
            "schema:streetAddress ?address.\n"
                "?address_link a schema:PostalAddress;\n"
                "schema:geo ?coordinates .\n"
                "?coordinates a schema:GeoCoordinates;\n"
                "schema:longitude ?longitude ;\n"
                "schema:latitude ?latitude .\n"
                f"FILTER (?dayOfWeek = \"{day}\" && ?openingTime <= \"{time}\" && ?closingTime > \"{time}\")\n"
                "}"
                )
    elif type == "city":
        search_query += (
            "SELECT ?restaurant ?name ?openingTime ?closingTime ?address\n"
            "WHERE {\n"
            "?restaurant a schema:Restaurant ;\n"
            "schema:name ?name;\n"
            "schema:address ?address_link;\n"
            "schema:openingHoursSpecification [\n"
            "schema:opens ?openingTime ;\n"
            "schema:closes ?closingTime ;\n"
            "schema:dayOfWeek ?dayOfWeek\n"
            "] .\n"
            "?address_link a schema:PostalAddress;\n"
            "schema:streetAddress ?address.\n"
                "?cooplink pwp:coopcycle_url ?coopurl;\n"
                "pwp:city ?city.\n"
                "?coopurl pwp:CanDeliverFoodOf ?restaurant;\n"
                f"FILTER (?city = \"{coordinates}\" && ?dayOfWeek = \"{day}\" && ?openingTime <= \"{time}\" && ?closingTime > \"{time}\")\n"
                "}"
                )

    return search_query
