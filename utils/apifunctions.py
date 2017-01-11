import sqlite3
import foursquare

#db = sqlite3.connect("data/dab.db", check_same_thread=False)
#d = db.cursor()

# =========== START ACCESSOR METHODS =============

def get_username(userid):
    q = 'SELECT username FROM users WHERE id =\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()
    
    return r[0][0]


def foursq(lat, lng):
    client = foursquare.Foursquare(client_id='IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK', client_secret='JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL')

    Lnuggets = client.venues.search(params={'query': 'chicken nuggets', 'll': lat+','+lng, 'radius': '1000'})
    locations = []
    #print(Lnuggets["venues"])
    for i in Lnuggets["venues"]:
        locations+=i["name"]
    test = ""
    for i in locations:
        test += i
    print(test)
    #print(locations)

foursq('40.705254579110886','-73.99236843350121')


# ========== END ACCESSOR METHODS ================
