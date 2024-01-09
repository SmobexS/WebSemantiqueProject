from prettytable import PrettyTable

def data_table(data, type):
    table = PrettyTable()
    table.field_names = data["head"]["vars"]
    if type == "city" :
        for binding in data["results"]["bindings"]:
            table.add_row([binding["restaurant_link"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"]])
    
    elif type == "price":
        for binding in data["results"]["bindings"]:
            table.add_row([binding["restaurant_link"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"], binding["minimum order price"]["value"], binding["distance from your location(m)"]["value"]])    
    
    else:
        for binding in data["results"]["bindings"]:
            table.add_row([binding["restaurant_link"]["value"], binding["name"]["value"], binding["openingTime"]["value"], binding["closingTime"]["value"], binding["address"]["value"], binding["distance from your location(m)"]["value"]])

    return(table)

def visualize_table (nbr_resultat, code_er, table):
    if code_er == 0:
        print("No restaurant is open at this time. Try an other time.")
    elif code_er == 1:
        print("No restaurant found in the given location and distance. Try an other location or distance.")
    elif code_er == 3:
        print("No restaurant found in the given city. Try an other city.")
    else:
        print(f"{nbr_resultat} restaurants are open at this time.")
        valide = False

        valid_nb = False
        while valid_nb == False :
            nb = input("How many restaurants do you want to see ? (All by default if you press Enter) : ") or nbr_resultat
            try :
                nb = int(nb)
                valid_nb = True
            except :
                print("Enter a valid number.")
                valid_nb = False
        
        min = 0

        while valide == False:

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