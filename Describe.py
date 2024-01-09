from TriplestoreFunctions import *
from RdfToSparql import *
from Query import main
from CoordOperations import *

def describe ():
    print("Welcome dear user.")
    print("Our application will help you to find an available restaurant that delivers food near you basing on your preferences.")
    print("Anwser this question to start using the application.")

    exit_val = False
    did_a_seararch = False

    while exit_val == False :

        d = input("To start a search enter 1.\nTo exit the application enter 2.\n")
        
        if d == "1":

            s = 0 

            while s != 1 :

                if did_a_seararch == False : 

                    usage_profile()
                    did_a_seararch = True

                else: 

                    conf = False

                    while conf == False:

                        other_search_dis = input("Do you want to make an other search (y/n): ") 

                        if other_search_dis.lower() == "y" :
                            
                            usage_profile()
                            conf = False
                            
                        elif other_search_dis.lower() == "n" :

                            print("Thank you for using our application.\nGood Bye.")
                            conf = True
                            exit_val = True
                            s=1

                        else :

                            print("Please chose 'y' for yes or 'n' for no.")
                            conf = False

        elif d == "2" :

            conf = False

            while conf == False :

                ed = input("Do you realy want to exit the application (y/n): ")
                if ed.lower() == "y" :
                    
                    conf = True
                    exit_val = True
                    print("Good Bye")

                elif ed.lower() == "n":

                    conf = True
                    exit_val =False
                
                else :

                    print("Please chose 'y' for yes or 'n' for no.")
                    conf = False

        else :

            print("Please chose '1' to start a research or '2' to exit.")
            exit_val = False
        

def register():

    reg_des = input ("Do you want to save your preferences for future uses or not (y/n): ")

    if reg_des.lower() == "y" :
        
        valide_name = False
        while valide_name ==False :
            name = input("Enter a full name : ")
            if verify_name (name):
                print("There is already a user preferece with this name. Try an other name.")
                valide_name = False
            else :
                valide_name = True

        valide_place = False
        while valide_place == False :
            location = input("Enter your adress : ")
            if valid_place(location):
                valide_place = True

                max_distance = input("Enter maximum distance in kilometers (5Km by default if you press Enter): ") or 5
                max_distance = float(max_distance)

                coords = get_coordinates(location)

                latitude = coords[0]
                longitude = coords[1]

            else:
                print("Invalid place. Please try again.")
                valide_place = False
        
        valide_codep = False
        while valide_codep == False :
            postalcode = input("Enter your postal code : ")
            if valid_postalcode(location):
                valide_codep = True

            else:
                print("Invalid postal code. Please try again.")
                valide_codep = False
                
            
        max_price = input("Enter the max price you prefer for your order (15 EUR by defaukt if you press Enter): ") or 15.0
        max_price = float(max_price)
        
        valid_rank = False
        while valid_rank == False :
            ranked_by = input("How do you prefer to rank the results of your research : \n1. By distance (By default if you press Enter)\n2. By price\n") or "distance"
            if ranked_by == "1" or ranked_by == "2":
                valid_rank = True
            else:
                print("Plese chose '1' or '2'")
                valid_rank = False

        graph = insert_user_graph(name, location, postalcode, max_distance, max_price, ranked_by, longitude, latitude)

        print("\nYour profile has been created. you can use your name in the futur to make your research.\n")

        return (graph)
    elif reg_des.lower() == "n" :

        return (None)
    
    else :

        print("Please chose 'y' for yes or 'n' for no.")
        register()


def usage_profile():

    acount_quet = input("Have you saved your preferences before (y/n): ")
    if acount_quet.lower() == "n":

        result = register()

        if result != None :
            
            #main() #preferences from graph
            print("preferences from graph")

        else :
            ranked_by = input("How do you want to rank the results of your research : \n1. By distance (By default if you press Enter)\n2. By price\n") or "distance"
            #main() #manuelle
            print("preferences manuelle")
    
    elif acount_quet.lower() == "y":
        
        valid_name = False

        while valid_name == False :

            name = input("Enter the full name that you have registerd with : ")
            if verify_name(name):

                valid_name = True
                profile = get_profile(name)

                #main()#preferences from graph
                print("preferences from graph")

            else :

                print("There is no user with this name : ", name, "\n please Enter a valid name.")

                exit_d = False

                while exit_d == False :

                    exit_des = input("Do you want to exit and try again (y/n) :")

                    if exit_des.lower()=="y":
                        
                        usage_profile()
                        exit_d = True
                        valid_name = True
                    
                    elif exit_des.lower()=="n":
                        
                        valid_name = False
                        exit_d = True
                    
                    else :

                        print("Please chose 'y' for yes or 'n' for no.")
                        exit_d = False

    else :

         print("Please chose 'y' for yes or 'n' for no.")
         usage_profile()

def verify_name(name):

    search_query = search_user(name)
    result = search_data(search_query, 'http://localhost:3030/Users/')

    if len(result ["results"]["bindings"]) != 0 :
        return name
    else:
        return False

def get_profile(name):
    search_query = get_user(name)
    result = search_data(search_query, 'http://localhost:3030/Users/')

    for binding in result["results"]["bindings"] :

        subject = "<" + binding["sub"]["value"] + ">"
        location = binding["location"]["value"]
        postalcode = binding["postalcode"]["value"]
        max_distance = binding["max_distance"]["value"]
        max_price = binding["max_price"]["value"]
        ranked_by = binding["ranked_by"]["value"]
        longitude = binding["longitude"]["value"]
        latitude =binding["latitude"]["value"]

    graph = info_user_to_graph(subject, name, location, postalcode, max_distance, max_price, ranked_by, longitude, latitude)
    
    return graph

def insert_user_graph(name, location, postalcode, max_distance, max_price, ranked_by, longitude, latitude):

    if ranked_by == '1':
        ranked_by = "distance"
    else :
        ranked_by = "price"
    
    insert_query = insert_query_user(name, location, postalcode, max_distance, max_price, longitude, latitude, ranked_by)
    insert_data(insert_query, 'http://localhost:3030/Users/')

    subject = f"<https://projectw9s.com/users/{name}>"

    graph = info_user_to_graph(subject, name, location, postalcode, max_distance, max_price, ranked_by, longitude, latitude)

    return graph

def info_user_to_graph (subject, name, location, postalcode, max_distance, max_price, ranked_by, longitude, latitude):

    turrtle_str = f"""
        @prefix schema: <http://schema.org/> .

        {subject} 
            a schema:Person ;
            schema:name "{name}";
            schema:address [
            a schema:PostalAddress ;
            schema:postalCode "{postalcode}" ;
            schema:addressLocality "{location}"
            ] ;
            schema:seeks [
                schema:priceSpecification [
                schema:maxPrice {max_price} ;
                schema:priceCurrency "EUR"
                ] ;
            schema:availableAtOrFrom [
                schema:geoWithin [
                    a schema:GeoCircle ;
                    schema:geoMidpoint [
                    schema:longitude {longitude} ;
                    schema:latitude {latitude}
                    ] ;
                    schema:geoRadius {max_distance}
                    ]
                ] ;
            schema:ranking "{ranked_by}"
            ] .
            """
    
    graph = ConjunctiveGraph()

    graph.parse(data=turrtle_str, format="turtle")

    print(graph.serialize(format="turtle"))

    return graph

describe()