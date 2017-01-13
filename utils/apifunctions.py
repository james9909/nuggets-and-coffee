import sqlite3
import foursquare
import geocoder
import config

def get_username(userid):
    q = 'SELECT username FROM users WHERE id =\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]

def getlatlng(address):
    g = geocoder.google(address)
    return g.latlng

def foursq(lat, lng):
    client = foursquare.Foursquare(client_id=config.keys["FOURSQUARE_CLIENT_ID"], client_secret=config.keys["FOURSQUARE_CLIENT_SECRET"])

    Lnuggets = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1609'})
    locations = []
    for i in Lnuggets["venues"]:
        locations.append(str(i["name"]))
    return locations

if __name__ == "__main__":
    config.load_keys()
    print(foursq(getlatlng("jamica queens")[0],getlatlng("jamica queens")[1]))
