import hashlib, os, json, random
import sqlite3, utils
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby
from utils import postManager, accountManager
from utils.apifunctions import foursq, getlatlng
import foursquare


app = Flask(__name__)

app.secret_key = os.urandom(32)
secret = 'secret_cookie_key'

@app.route("/")
def index():
    #print(client.user())
    #print(Lnuggets[:10])
    if (secret in session):
        name = session[secret]
        return render_template('main.html', logged_status="true", type=utils.accountManager.get_type(session[secret])[0])
#        return render_template('mainCoffee.html')
    return render_template('base.html')

@app.route("/home")
def return_home():
    if (secret in session):
        return render_template('main.html', logged_status="true", type=utils.accountManager.get_type(session[secret])[0])
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

        if(are_u_in[0] == True):
            session[secret]=given_user
            return render_template('main.html', logged_status="true", type=utils.accountManager.get_type(given_user)[0])

    return render_template('login.html', action='login', logged_status="false")

@app.route("/logout")
def log_em_out():
    session.pop(secret)
    return redirect(url_for("index"))

@app.route("/register", methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        wanted_user = request.form['username']
        wanted_pass1 = request.form["password"]
        wanted_pass2 = request.form["passconfirm"]
        type_selected = request.form["types"]

        hashPassObj1 = hashlib.sha1()
        hashPassObj1.update(wanted_pass1)
        hashed_pass1 = hashPassObj1.hexdigest()

        hashPassObj2 = hashlib.sha1()
        hashPassObj2.update(wanted_pass2)
        hashed_pass2 = hashPassObj2.hexdigest()

        is_user_now = utils.accountManager.register(wanted_user, hashed_pass1, hashed_pass2, type_selected)

        if(is_user_now[0] == True):
            session[secret] = wanted_user
            return render_template('main.html', logged_status="true", type=utils.accountManager.get_type(wanted_user)[0])

    return render_template('login.html', action='register', logged_status="false")

@app.route("/favorites")
def fav_page():
    return render_template('mainNuggets.html', logged_status="true")

@app.route("/mainNuggets")
def mainNuggets():
    return render_template('mainNuggets.html', logged_status="true")

@app.route("/mainCoffee")
def mainCoffee():
    return render_template('mainCoffee.html', logged_status="true")

@app.route("/Nlocation", methods=['GET','POST'])
def Nlocation():
    naddress = ""
    spots = {}
    a = ''
    if request.method == 'POST':
        a = request.form['address']
        for i in a:
            if(i==' '):
                naddress+="%20"
            else:
                naddress+=i
        spots = foursq(getlatlng(a)[0],getlatlng(a)[1],"nugget")
    #print(spots)
    return render_template('Nlocation.html', name = str(a), naddress=naddress, spots=spots)

@app.route("/Clocation", methods=['GET','POST'])
def Clocation():
    naddress = ""
    spots = {}
    a = ''
    if request.method == 'POST':
        a = request.form['address']
        for i in a:
            if(i==' '):
                naddress+="%20"
            else:
                naddress+=i
        spots = foursq(getlatlng(a)[0],getlatlng(a)[1],"coffee")
 
    return render_template('Clocation.html', name = str(a), naddress=naddress, spots=spots)

    
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

@app.route("/createPost", methods=["POST"])
def createPost():
    username = session["username"]
    title = request.form["title"]
    content = request.form["content"]

    postid = postManager.createPost(username, title, content)
    return redirect("/forum/" + postid)


if __name__ == "__main__":
    # Generate and store secret key if it doesn't exist
    with open(".secret_key", "a+b") as f:
        secret_key = f.read()
        if not secret_key:
            secret_key = os.urandom(64)
            f.write(secret_key)
            f.flush()
        app.secret_key = secret_key

    utils.config.load_keys()
    app.debug = True
    app.run()
