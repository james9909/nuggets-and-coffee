import hashlib
import os
import utils
from flask import Flask, jsonify, render_template, session, request, redirect, url_for
from itertools import count, groupby
from utils import postManager, accountManager
from utils.apifunctions import foursq, getlatlng

app = Flask(__name__)

@app.route("/")
def index():
    if "username" in session:
        name = session["username"]
        return render_template("main.html", type=utils.accountManager.get_type(name)[0])
        # return render_template('mainCoffee.html')
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha1(password).hexdigest()

        success, message = utils.accountManager.authenticate(username, hashed_password)

        if success:
            session["username"] = username
        return jsonify({"success": success, "message": message})

    return render_template("login.html", action="login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["passconfirm"]
        type_selected = request.form["types"]

        success, message = utils.accountManager.register(username, password, confirm_password, type_selected)

        return jsonify({"success": success, "message": message})

    return render_template("login.html", action="register")

@app.route("/favorites")
def fav_page():
    return render_template("mainNuggets.html")

@app.route("/mainNuggets")
def mainNuggets():
    return render_template("mainNuggets.html")

@app.route("/mainCoffee")
def mainCoffee():
    return render_template("mainCoffee.html")

@app.route("/Nlocation", methods=["GET", "POST"])
def Nlocation():
    naddress = ""
    spots = {}
    a = ""
    name = ""
    works = True
    if request.method == "POST":
        a = request.form["address"]
        for i in a:
            if i == " ":
                naddress+="%20"
                name+="-"
            else:
                naddress+=i
                name+=i
        try:
            spots = foursq(getlatlng(a)[0],getlatlng(a)[1],"nugget")
        except:
            works = False
    return render_template("Nlocation.html", name = name, naddress=naddress, spots=spots, works=works)

@app.route("/Clocation", methods=["GET", "POST"])
def Clocation():
    naddress = ""
    spots = {}
    a = ""
    name = ""
    works = True
    if request.method == "POST":
        a = request.form["address"]
        for i in a:
            if(i==" "):
                naddress+="%20"
                name+="-"
            else:
                naddress+=i
                name+=i
        try:
            spots = foursq(getlatlng(a)[0],getlatlng(a)[1],"coffee")
        except:
            works = False
#print(spots)
    return render_template("Clocation.html", name = name, naddress=naddress, spots=spots, works=works)


@app.route("/forum")
@app.route("/forum/<postid>")
def forum(postid=None):
    # checks if a valid postid was supplied
    if not postid or not postManager.checkid(postid):
        posts = postManager.getPosts()
        return render_template("forum.html", posts=posts)

    postinfo = postManager.getPost(postid)
    replies = postManager.getReplies(postid)
    return render_template("post.html", postinfo=postinfo, replies=replies)

@app.route("/createPost", methods=["GET","POST"])
def createPost():
    if request.method == "GET":
        return render_template("createPost.html")
    else:
        username = session["username"]
        title = request.form["title"]
        content = request.form["content"]
        postid = postManager.createPost(username, title, content)
    return redirect("/forum/" + str(postid))

@app.route("/recipes")
def show_recipes():
    #type_r = utils.accountManager.get_type(secret[session])
    r_images = utils.apifunctions.get_image(utils.apifunctions.get_recipes("coffee cake"))
    #r_title = utils.apifunctions.get_titles(utils.apifunctions.get_titles("coffee cake"))
    r_urls = utils.apifunctions.get_image(utils.apifunctions.get_source("coffee cake"))

    return render_template("recipes.html", recipe_images = r_images, recipe_len = len(r_images), logged_status="true")

@app.route("/reply", methods=["POST"])
def reply():
    if "username" in session:
        username = session["username"]
    else:
        username = "anonymous"
    postid = request.form["postid"]
    content = request.form["content"]
    postManager.makeReply(username, postid, content)
    return redirect("/forum/"+str(postid))

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
