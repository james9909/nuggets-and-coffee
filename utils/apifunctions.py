import config

import foursquare
import geocoder
import requests

def getlatlng(address):
    g = geocoder.google(address)
    return g.latlng

def foursq(lat, lng, NC):
    client = foursquare.Foursquare(client_id=config.keys["FOURSQUARE_CLIENT_ID"], client_secret=config.keys["FOURSQUARE_CLIENT_SECRET"])
    if NC=="nugget":
        L = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1000'})
    else:
        L = client.venues.search(params={'query': 'coffee', 'll': str(lat)+','+str(lng), 'radius': '1000'})

    locations = []
    for i in L["venues"]:
        location = {
            "name": i["name"],
            "lat": i["location"]["labeledLatLngs"][0]["lat"],
            "lng": i["location"]["labeledLatLngs"][0]["lng"],
            "address": ", ".join(i["location"]["formattedAddress"])[:-2],
            "url": i.get("url", "N/A"),
            "phone": i["contact"].get("formattedPhone", "N/A")
        }
        locations.append(location)
    return locations

# RECIPES

def get_recipes(query):
    headers = {'key':config.keys["RECIPE_KEY"],'q':query}
    response = requests.get("http://food2fork.com/api/search", headers)
    recipes = response.json()['recipes']
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


#print(get_titles(get_recipes('coffee')))
#print(get_image(get_recipes('coffee')))

if __name__ == "__main__":
    config.load_keys()
    location = "Stuy"
    try:
        foursq(getlatlng(location)[0], getlatlng(location)[1], "coffee")
    except:
        print("doesn't work")
