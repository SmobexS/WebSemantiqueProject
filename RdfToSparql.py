from rdflib import URIRef, Literal, BNode
from UnicodeToStr import *
import requests

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


def get_by_place(day, time, type, coordinates, max_distance):
    search_query = (
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
        "PREFIX pwp:<https://ProjectW9s.com/predicate/>\n"
        "PREFIX pwo:<https://ProjectW9s.com/object/>\n"
        "PREFIX pws:<https://ProjectW9s.com/subject/>\n"
        "PREFIX schema: <http://schema.org/>\n"
        "PREFIX geof: <http://www.opengis.net/ont/geosparql#>\n"
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
    )

    if type == "address":
        latitude, longitude = get_lat_long_for_place(coordinates)
    elif type == "geocord":
        latitude = coordinates[0]
        longitude = coordinates[1]
    elif type == "city":
        latitude, longitude = get_lat_long_for_place(coordinates)

    if latitude is not None and longitude is not None:
        if type == "address" or type == "geocord":
            search_query += (
                "?address_link a schema:PostalAddress;\n"
                "schema:geo ?coordinates .\n"
                "?coordinates a schema:GeoCoordinates;\n"
                "schema:longitude ?longitude ;\n"
                "schema:latitude ?latitude .\n"
                f"FILTER (geof:distance(?coordinates, geof:point({longitude}, {latitude}), {max_distance})) .\n"
                f"FILTER (?dayOfWeek = \"{day}\" && ?openingTime <= \"{time}\" && ?closingTime > \"{time}\")\n"
                "}"
            )
        elif type == "city":
            search_query += (
                "?cooplink pwp:coopcycle_url ?coopurl;\n"
                "pwp:city ?city.\n"
                "?coopurl pwp:CanDeliverFoodOf ?restaurant;\n"
                f"FILTER (?city = \"{coordinates}\" && ?dayOfWeek = \"{day}\" && ?openingTime <= \"{time}\" && ?closingTime > \"{time}\")\n"
                "}"
            )
    else:
        if type == "address":
            print(f"Unable to get coordinates for the place: {coordinates}")
        elif type == "geocord":
            print(f"Unable to get coordinates for the latitude: {latitude} and longitude: {longitude}")
        elif type == "city":
            print(f"Unable to get city: {coordinates}")
    return search_query


def get_lat_long_for_place(coordinates):
    nominatim_endpoint = "https://nominatim.openstreetmap.org/search"
    params = {"q": coordinates, "format": "json"}
    headers = {"User-Agent": "YourApp/1.0"}

    try:
        response = requests.get(nominatim_endpoint, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            return None, None
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
        return None, None
    


def get_by_max_price(day, time, max_price=None):
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ns: <http://example.org/ontology/restaurant#>

    SELECT ?restaurant ?name ?delivery_cost
    WHERE {
        ?restaurant rdf:type ns:Restaurant .
        ?restaurant ns:isOpenAt ?openTime .
        ?restaurant ns:hasDelivery true .
        ?restaurant ns:deliveryCost ?delivery_cost .

        FILTER(?openTime = "%s" && ?delivery_cost <= %s)
    }
    """ % (time, max_price)

    return query
