import hashlib, os, json, random
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby
import foursquare

app = Flask(__name__)

app.secret_key = os.urandom(32)
secret = 'secret_cookie_key'

client = foursquare.Foursquare(client_id='IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK', client_secret='JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL')

Lnuggets = client.venues.search(params={'query': 'chicken nuggets'})
#========================================ROUTAGE

#either shows user their home (stories edited by them), or redirect to login
@app.route("/")
def index():
    print(client.user())
    print(Lnuggets[:10])
    if (secret in session):
        name = session[secret]
        return render_template('index.html')
    return render_template('base.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
