import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from rdflib import Graph, ConjunctiveGraph, Namespace, URIRef, Literal
from collections import defaultdict

def JsonLDScraper (json_file) :
    data = pd.read_json(json_file)
    graph = ConjunctiveGraph()

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

    print("Le nombre de cooperatives : ", len(coops_restaurants_urls))

    for coop_restaurants_url in coops_restaurants_urls:

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
                    all_restaurants[coop_restaurants_url][restaurant_url] = json_ld_data
                except json.JSONDecodeError:
                    print("Erreur lors du décodage JSON-LD")

    return(all_restaurants)
