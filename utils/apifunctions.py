import config

import foursquare
import geocoder
import requests

def getlatlng(address):
    g = geocoder.google(address)
    return g.latlng

def foursq(lat, lng, NC):
    client = foursquare.Foursquare(client_id=config.keys["IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK"], client_secret=config.keys["JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL"])
    if NC=="nugget":
        L = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1000'})
    else:
        L = client.venues.search(params={'query': 'coffee', 'll': str(lat)+','+str(lng), 'radius': '1000'})
#    print L["venues"][8]["contact"]["formattedPhone"]
 #   print("Made it here!")

    locations = {}
    for i in L["venues"]:
        coords = []
        coords.append(str(i["location"]["labeledLatLngs"][0]["lat"]))
        coords.append(str(i["location"]["labeledLatLngs"][0]["lng"]))
        address = ""
        for j in i["location"]["formattedAddress"]:
            address += j + ", "
        #coords.append(i["location"]["formattedAddress"])
        coords.append(address[:-2])
        try: #because not every location has a number or website avail
            coords.append(str(i["url"]))
        except:
            coords.append("nope")
        try:
            coords.append(str(i["contact"]["formattedPhone"]))
        except:
            coords.append("nope")
        locations[i["name"]] = coords
    print locations
    return locations

#print(foursq(100,100,"nugget"))

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
