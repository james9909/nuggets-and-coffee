import sqlite3
import foursquare
import geocoder

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

    Lnuggets = client.venues.search(params={'query': 'chicken nuggets', 'll': str(lat)+','+str(lng), 'radius': '1609'})
    locations = []
    for i in Lnuggets["venues"]:
        locations.append(str(i["name"]))
    return locations

if __name__ == "__main__":
    print(foursq(getlatlng("jamica queens")[0],getlatlng("jamica queens")[1]))
