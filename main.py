from query import *

class Main:

    def __init__(self):
        self.query = Query()

    def query_executor(self):
        parser = argparse.ArgumentParser(description="CoopCycle restaurants query program:")
        parser.add_argument("--rank-by", choices=["distance", "price"], help="Ranking restaurants by distance or price")
        parser.add_argument("--user-preferences", action="store_true", help="User preferences from .ttl file")
        args = parser.parse_args()

        if args.user_preferences:
            pref_uri = "https://www.emse.fr/~zimmermann/Teaching/SemWeb/Project/pref-charpenay.ttl"
            user_preferences = self.query.get_user_preferences(pref_uri)

            if 'seller' in user_preferences:
                print("User is looking for restaurants near:", user_preferences.get('location', "Not specified"))
                print("User is looking for restaurants from seller:", user_preferences['seller'])
                print("User has a maximum budget of", user_preferences['max_price'][0], user_preferences['max_price'][1])

                if args.rank_by in ["distance", "price"]:
                    day, time =self.query.get_date_time()

                    if 'location' in user_preferences:
                        coordinates = user_preferences['location'][:2]
                        max_distance = user_preferences['location'][2]
                    else:
                        coordinates = None
                        max_distance = None

                    if args.rank_by == "distance":
                        self.query.get_restaurants_by_ranking(day, time, coordinates, max_distance, "distance")
                    elif args.rank_by == "price" and 'max_price' in user_preferences:
                        max_price = user_preferences['max_price'][0]
                        self.query.get_restaurants_by_ranking(day, time, coordinates, max_distance, "price", max_price)
                    else:
                        print("Invalid ranking option or user preferences. Please check your input.")
                else:
                    print("Invalid ranking option. Please choose 'distance' or 'price'.")
            else:
                print("Seller information not found in user preferences.")
        else:
            if args.rank_by:
                print("Error: When using --rank-by, --user-preferences is required.")
            else:
                print("Error: --rank-by option is required.")




if __name__ == "__main__":
    main = Main()
    main.query_executor()