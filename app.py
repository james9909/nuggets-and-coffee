import hashlib, os, json, random, utils.accountManager
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby
from utils import postManager, accountManager
import foursquare

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
        return render_template('mainCoffee.html')
    return render_template('base.html')

@app.route("/login", methods=['GET', 'POST'])
def log_in():
    if request.method == "POST":
        given_user = request.form["username"]
        given_pass = request.form["password"]
        
        hashPassObj = hashlib.sha1()
        hashPassObj.update(given_pass)
        hashed_pass = hashPassObj.hexdigest()

        are_u_in = utils.accountManager.authenticate(given_user, hashed_pass)

        print(are_u_in)

        if(are_u_in[0] == True):
            session[secret]=given_user
            return render_template('mainCoffee.html', logged_status="true")

    return render_template('login.html', action='login', logged_status="false")

@app.route("/logout")
def log_em_out():
    session
    session.pop(secret)
    return redirect(url_for("index")) 

@app.route("/register", methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        wanted_user = request.form['username']
        wanted_pass1 = request.form["password"]
        wanted_pass2 = request.form["passconfirm"]

        hashPassObj1 = hashlib.sha1()
        hashPassObj1.update(wanted_pass1)
        hashed_pass1 = hashPassObj1.hexdigest()
        
        hashPassObj2 = hashlib.sha1()
        hashPassObj2.update(wanted_pass2)
        hashed_pass2 = hashPassObj2.hexdigest()

        is_user_now = utils.accountManager.register(wanted_user, hashed_pass1, hashed_pass2)

        print(is_user_now)

        if(is_user_now == True):
            session[secret] = wanted_user
            return redirect(url_for("index")) #redirect(url_for("log_em_in"))

    return render_template('login.html', action='register', logged_status="false")

@app.route("/favorites")
def fav_page():
    return render_template('mainNuggets.html', logged_status="true")

@app.route("Nlocation", methods=['POST'])
def Nlocation():
    address = request.form('address')
    naddress = ""
    for i in address:
        if(i==' '):
            naddress+="%20"
        else:
            naddress+=i
    print(naddress)
    return render_template('Nlocation.html', naddress=address)

@app.route("/forum")
@app.route("/forum/<postid>") 
def forum(postid=None):
    # checks if a valid postid was supplied
    if not postid or not postManager.checkid(post):
        posts = postManager.getPosts()
        return render_template('forum.html', posts=posts)

    postinfo = postManager.getPost(postid)
    comments = postManager.getReplies(postid)
    return render_template('post.html', postinfo=postinfo, comments=comments)


if __name__ == "__main__":
    # Generate and store secret key if it doesn't exist
    with open(".secret_key", "a+b") as f:
        secret_key = f.read()
        if not secret_key:
            secret_key = os.urandom(64)
            f.write(secret_key)
            f.flush()
        app.secret_key = secret_key

    app.debug = True
    app.run()
