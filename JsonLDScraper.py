import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from collections import defaultdict
from urllib.parse import urlparse , urlunparse

def parse_url(url):
    parsed_url = urlparse(url)
    main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return(main_url)

def parse_url_contry(url):
    parsed_url = urlparse(url)
    main_url_with_path = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return(main_url_with_path)


def JsonLDScraper (json_file) :
    data = pd.read_json(json_file)

    all_restaurants = defaultdict(lambda : defaultdict(dict))

    coops_restaurants_urls = []

    for index, row in data.iterrows():

        if type(row['coopcycle_url'])==str :
            coop_url = row['coopcycle_url']
            country = row['country'] if row['country'] else 'fr'
            coop_restaurants_url = f"{coop_url}/{country}/shops?type=restaurant"
            coops_restaurants_urls.append(coop_restaurants_url)
        else :
            continue

    for coop_restaurants_url in coops_restaurants_urls:

        coop_url = parse_url(coop_restaurants_url)
        coop_url_contry = parse_url_contry(coop_restaurants_url)

        response = requests.get(coop_restaurants_url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        restaurants_divs = soup.find_all('div', class_='restaurant-item')

        for restaurant_div in restaurants_divs:
            restaurant = restaurant_div.find('a')['href']
            restaurant_url = f"{coop_url}{restaurant}"

            restaurant_response = requests.get(restaurant_url)
            restaurant_html_content = restaurant_response.text

            restaurant_soup = BeautifulSoup(restaurant_html_content, 'html.parser')
            json_ld = restaurant_soup.find('script', {'type': 'application/ld+json'})

            if json_ld:
                try:
                    json_ld_data = json.loads(json_ld.string)

                    idd = json_ld_data["@id"]=restaurant_url
                    json_ld_data["@id"] = idd
                    address = json_ld_data["address"]["@id"].replace("/api/addresses", coop_url_contry +"/addresses")
                    json_ld_data["address"]["@id"] = address
         
                    all_restaurants[coop_url][restaurant_url] = json_ld_data
                except json.JSONDecodeError:
                    print("Erreur lors du décodage JSON-LD")

    with open('JsonLD.txt', 'w', encoding="utf-8") as file:
        for cop, restos in all_restaurants.items():
            file.write(f"Coop \" {cop} \" :\n")
            for resto, jsonld in restos.items():
                file.write(f"\t Restaurant \" {resto} \" :\n")
                file.write(f"\t\t {jsonld}\n")
                file.write("\t==========================================================================\n")
            file.write("\n==========================================================================\n\n")

    return(all_restaurants)

