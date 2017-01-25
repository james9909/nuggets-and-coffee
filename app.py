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
            print("login success!")
            session["username"] = username

        else:
            print("login failed")

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

        success, message = utils.accountManager.register(username, password, confirm_password)

        response = {"success": success, "message": message}

        if success:
            session["username"] = username
            response["redirect"] = "/"

        return jsonify(response)

    return render_template("login.html", action="register")

@app.route("/favorites")
def fav_page():
    if "username" in session:
        return render_template("main.html", type=utils.accountManager.get_type(session["username"][0]))
    else:
        return redirect(url_for("login"))

@app.route("/mainNuggets")
def main_nug():
    if "username" in session:
        return render_template("mainNuggets.html")
    else:
        return redirect(url_for("login"))

@app.route("/mainCoffee")
def main_coffee():
    if "username" in session:
        return render_template("mainCoffee.html")
    else:
        return redirect(url_for("login"))

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

@app.route("/recipes", methods=["GET", "POST"])
def show_recipes():
    if "username" in session:
        if request.method == "POST":
            type_r = request.form["food_query"]
            r_images = utils.apifunctions.get_image(utils.apifunctions.get_recipes(type_r))
            r_titles = utils.apifunctions.get_titles(utils.apifunctions.get_recipes(type_r))
            r_urls = utils.apifunctions.get_source(utils.apifunctions.get_recipes(type_r))
            return render_template("recipes.html", recipe_images = r_images, recipe_titles = r_titles, recipe_urls = r_urls, recipe_len = len(r_images), posted="true")

        else:
            return render_template("recipes.html", posted = "false")
    else:
        return redirect(url_for("login"))

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

@app.route("/updateType", methods=["POST"])
def update_type():
    _type = request.form["type"]
    utils.accountManager.updateInfo(session.get("username"), type=_type)
    return jsonify({"success": 1, "message": "Preference set to %s" % _type})

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
