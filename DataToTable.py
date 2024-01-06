from prettytable import PrettyTable

def data_table(data):
    table = PrettyTable()
    table.field_names = data["head"]["vars"]
    for binding in data["results"]["bindings"]:
        table.add_row([binding["restaurant"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"]])

    return(table)