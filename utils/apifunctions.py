import config

import foursquare
import geocoder
import requests

def getlatlng(address):
    g = geocoder.google(address)
    return g.latlng

def foursq(lat, lng, NC):
    client = foursquare.Foursquare(client_id=config.keys["FOURSQUARE_CLIENT_ID"], client_secret=config.keys["FOURSQUARE_CLIENT_SECRET"])

    if NC == "nugget":
        query = "chicken nuggets"
    else:
        query = "coffee"

    venues = client.venues.search(params={'query': query, 'll': "%s,%s" % (lat, lng), 'radius': '1000'})

    locations = []
    if len(venues["venues"]) == 0:
        return locations

    for venue in venues["venues"][:10]: # Limit to ten venues
        location = {
            "name": venue["name"],
            "lat": venue["location"]["labeledLatLngs"][0]["lat"],
            "lng": venue["location"]["labeledLatLngs"][0]["lng"],
            "address": ", ".join(venue["location"]["formattedAddress"])[:-2],
            "url": venue.get("url", "N/A"),
            "phone": venue["contact"].get("formattedPhone", "N/A")
        }
        locations.append(location)
    return locations

# RECIPES

def get_recipes(query):
    headers = {"key":config.keys["RECIPE_KEY"],"q":query}
    response = requests.get("http://food2fork.com/api/search", headers)
    try:
        recipes = response.json()["recipes"]
    except:
        recipes = []
    return recipes

def get_titles(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['title'].encode('utf-8')
    return titles

def get_source(recipes):
    sources = {}
    for i in range(len(recipes)):
        sources[i] = recipes[i]['source_url'].encode('utf-8')
    return sources

def get_f2f(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['f2f_url'].encode('utf-8')
    return titles

def get_image(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['image_url'].encode('utf-8')
    return titles

def get_rank(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['social_rank']
    return titles

def get_pub(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['publisher'].encode('utf-8')
    return titles

def get_puburl(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = recipes[i]['publisher_url'].encode('utf-8')
    return titles
