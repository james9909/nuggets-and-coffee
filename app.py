import hashlib, os, json, random
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby
#import foursquare

app = Flask(__name__)

app.secret_key = os.urandom(32)
secret = 'secret_cookie_key'

#client = foursquare.Foursquare(client_id='IVAQCEMVQ3OR00SDOCEZR4AQ5KEQXXRWKQYRAHLIVM50QWKK', client_secret='JGOJZECQYXHNPVSIH4WK2N5HTNECAJAWFL3RF2E5J03IZRNL')

#Lnuggets = client.venues.search(params={'query': 'chicken nuggets'})
#========================================ROUTAGE

#either shows user their home (stories edited by them), or redirect to login
@app.route("/")
def index():
    #print(client.user())
    #print(Lnuggets[:10])
    if (secret in session):
        name = session[secret]
        return render_template('index.html')
    return render_template('base.html')

@app.route("/login")
def login():
    #given_user = request.form["username"]
    #given_pass = request.form["password"]

    #hashPassObj = hashlib.sha1()
    #hashPassObj.update(given_pass)
    #hashed_pass = hashPassObj.hexdigest()

    #are_u_in = utils.auth.login(given_user, hashed_pass)

    #if(are_u_in == True):
     #   session[secret]=given_user
     #   return redirect(url_for('index'))
    return render_template('login.html', action='login')

@app.route("/register")
def register():
    return render_template('login.html', action='register')

if __name__ == "__main__":
    app.debug = True
    app.run()
