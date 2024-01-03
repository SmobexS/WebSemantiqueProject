from rdflib import Graph, URIRef, Literal, BNode, Namespace

def format_term(term):
    if isinstance(term, URIRef):
        return f"<{term}>"
    elif isinstance(term, Literal):
        if term.language:
            return f'"{term}"@{term.language}'
        elif term.datatype:
            return f'"{term}"^^<{term.datatype}>'
        else:
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

def generate_delete_query(graph):
    delete_query = "DELETE DATA {\n"

    for subj, pred, obj in graph:
        subject = format_term(subj)
        predicate = format_term(pred)
        obj = format_term(obj)

        delete_query += f"  {subject} {predicate} {obj} .\n"

    delete_query += "}"

    return delete_query

def generate_update_query(o_triples, n_triples):
    update_query = "INSERT DATA {\n"

    update_query += f"  {o_triples[0]} {o_triples[1]} {o_triples[2]} .\n"

    update_query += "};\n\n"

    update_query += "DELETE DATA {\n"
    
    update_query += f"  {n_triples[0]} {n_triples[1]} {n_triples[2]} .\n"

    update_query += "}"

    return update_query