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

def foursq(lat, lng, NC):
    client = foursquare.Foursquare(client_id='IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK', client_secret='JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL')
    if NC=="nugget":
        L = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1000'})
    else:
        L = client.venues.search(params={'query': 'coffee', 'll': str(lat)+','+str(lng), 'radius': '1000'})
    #print L["venues"][8]["contact"]["formattedPhone"]
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
    location = "Stuy"
    try:
        foursq(getlatlng(location)[0], getlatlng(location)[1], "coffee")
    except:
        print("doesn't work")
