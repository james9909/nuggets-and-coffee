import sqlite3, foursquare, geocoder
import config, requests

def get_username(userid):
    q = 'SELECT username FROM users WHERE id =\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

def getlatlng(address):
    g = geocoder.google(address)
    return g.latlng

def foursq(lat, lng):
    client = foursquare.Foursquare(client_id='IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK', client_secret='JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL')

    Lnuggets = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1000'})
    locations = {}
    for i in Lnuggets["venues"]:
        coords = []
        coords.append(str(i["location"]["labeledLatLngs"][0]["lat"]))
        coords.append(str(i["location"]["labeledLatLngs"][0]["lng"]))
        locations[str(i["name"])] = coords
    return locations


# RECIPES

def get_recipes(query):
    headers = {'key':'a8474350b415ca27e934104adaffa683','q':query}
    response = requests.get("http://food2fork.com/api/search", headers)
    recipes = response.json()['recipes']
    return recipes

def get_titles(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = str(recipes[0]['title'])
    return titles

def get_source(recipes):
    sources = {}
    for i in range(len(recipes)):
        sources[i] = str(recipes[0]['source_url'])
    return sources

def get_f2f(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = str(recipes[0]['f2f_url'])
    return titles

def get_image(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = str(recipes[0]['image_url'])
    return titles

def get_rank(recipes):
    titles = {}
    for i in range(len(recipes)):
        titles[i] = str(recipes[0]['social_rank'])
    return titles

#print(get_titles(get_recipes('chicken')))

if __name__ == "__main__":
    config.load_keys()
    
