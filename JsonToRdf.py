from rdflib import Namespace, Literal, ConjunctiveGraph, URIRef
import pandas as pd
import requests

pwss = Namespace("https://ProjectW9s.com/subject/")
pwso = Namespace("https://ProjectW9s.com/object/")
pwsp = Namespace("https://ProjectW9s.com/predicate/")

def json2rdf (link) :

    graph = ConjunctiveGraph()

    response = requests.get(link)

    if response.status_code == 200:
        
        data = response.json()
        data = pd.DataFrame(data)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return graph

    for index, row in data.iterrows():

        subject = "ENT"+row['city'].upper().replace(" ","_")[:3]+str(index)
        
        if str(row['city'])!='nan' :
            city = row['city']
            graph.add((pwss[subject], pwsp.city, Literal(city))) 

        if type(row['coopcycle_url'])==str :
            coopcycle_url = row['coopcycle_url'].strip()
            graph.add((pwss[subject], pwsp.coopcycle_url, URIRef(coopcycle_url)))

        if str(row['country'])!='nan' :
            country = row['country']
            graph.add((pwss[subject], pwsp.country, Literal(country)))

        if type(row['facebook_url'])==str :
            facebook_url = row['facebook_url'].strip()
            graph.add((pwss[subject], pwsp.facebook_url, URIRef(facebook_url)))

        if str(row['latitude'])!='nan' :
            latitude = row['latitude']
            graph.add((pwss[subject], pwsp.latitude, Literal(latitude)))

        if str(row['longitude'])!='nan' :
            longitude = row['longitude']
            graph.add((pwss[subject], pwsp.longitude, Literal(longitude)))

        if str(row['mail'])!='nan' :
            mail = row['mail']
            graph.add((pwss[subject], pwsp.mail, Literal(mail)))

        if str(row['name'])!='nan' :
            name = row['name']
            graph.add((pwss[subject], pwsp.name, Literal(name)))

        if str(row['text'])!='nan' :
            text = row['text']
            for ind, rt in text.items():
                graph.add((pwss[subject], pwsp.text, Literal(rt.replace("\"", "\'"), lang=ind)))

        if type(row['url'])==str :
            url = row['url'].strip()
            graph.add((pwss[subject], pwsp.url, URIRef(url)))

        if type(row['instagram_url'])==str :
            instagram_url = row['instagram_url'].strip()
            graph.add((pwss[subject], pwsp.instagram_url, URIRef(instagram_url)))

        if type(row['twitter_url'])==str :
            twitter_url = row['twitter_url'].strip()
            graph.add((pwss[subject], pwsp.twitter_url, URIRef(twitter_url)))

        if str(row['logo_src'])!= 'nan' :
            logo_src = row['logo_src']
            graph.add((pwss[subject], pwsp.logo_src, Literal(logo_src)))

        if type(row['delivery_form_url'])==str :
            delivery_form_url = row['delivery_form_url'].strip()
            graph.add((pwss[subject], pwsp.delivery_form_url, URIRef(delivery_form_url)))

        graph.add((pwss[subject], pwsp.CoopOf, URIRef("https://coopcycle.org/")))

    graph.serialize(destination='output.ttl', format='turtle', encoding="utf-8")

    return(graph)
