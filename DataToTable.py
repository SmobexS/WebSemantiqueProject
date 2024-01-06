from prettytable import PrettyTable

def data_table(data):
    table = PrettyTable()
    table.field_names = data["head"]["vars"]
    for binding in data["results"]["bindings"]:
        table.add_row([binding["restaurant"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"]])

    return(table)

def visualize_table (nbr_resultat, table):
    if nbr_resultat == 0:
        print("No restaurant is open at this time. Try an other time.")
    else:
        print(f"{nbr_resultat} restaurants are open at this time.")
        valide = False

        nb = input("How many restaurants do you want to see ? (All by default if you press Enter) : ") or nbr_resultat
        
        min = 0

        while valide == False:
            nb = int(nb)
            if nb >= nbr_resultat:
                nb = nbr_resultat
                valide = True

            table_print = table[min:nb+1]

            print(table_print)

            if nb < nbr_resultat:
                d = input("Do you want to see more restaurants ? (y/n) : ")
                if d.lower() == "y":
                    min = nb + 1
                    nb += 10
                else:
                    valide = True