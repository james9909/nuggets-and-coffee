import hashlib
import os
import utils
import random
from flask import Flask, jsonify, render_template, session, request, redirect, url_for
from itertools import count, groupby
from utils import postManager, accountManager
from utils.apifunctions import foursq, getlatlng
import api

app = Flask(__name__)
app.register_blueprint(api.api, url_prefix="/api")

@app.route("/")
def index():
    if "username" in session:
        name = session["username"]
        type=utils.accountManager.get_type(name)[0]
        if (type == "coffee"):
            return render_template("mainCoffee.html")
        elif (type == "nuggets"):
            return render_template("mainNuggets.html")
    return redirect(url_for("login"))

@app.route("/login")
def login():
    with open('pics.txt', 'r') as myfile:
        data=myfile.read().replace("\n", "").split(",")
    nc = []
    for i in range(0, 12):
        temp = random.choice(data)
        nc.append(temp)
        try:
            data.remove(temp+",")
        except:
            data.remove(temp)
    return render_template("login.html", nc=nc)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register")
def create_account():
    with open('pics.txt', 'r') as myfile:
        data=myfile.read().replace("\n", "").split(",")
    nc = []
    for i in range(0, 12):
        temp = random.choice(data)
        nc.append(temp)
        try:
            data.remove(temp+",")
        except:
            data.remove(temp)

    return render_template("register.html", nc=nc)

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
    if "username" in session:
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
    else:
        return redirect(url_for("login"))

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
            f_urls = utils.apifunctions.get_f2f(utils.apifunctions.get_recipes(type_r))
            r_rank = utils.apifunctions.get_rank(utils.apifunctions.get_recipes(type_r))
            p_ub = utils.apifunctions.get_pub(utils.apifunctions.get_recipes(type_r))
            p_url = utils.apifunctions.get_puburl(utils.apifunctions.get_recipes(type_r))
            return render_template("recipes.html", recipe_images = r_images, recipe_titles = r_titles, recipe_urls = r_urls, recipe_len = len(r_images), f2f_urls = f_urls,rankings = r_rank, posted="true", valueq=type_r, pubs = p_ub, puburls = p_url)

        else:
            return render_template("recipes.html", posted = "false", valueq="Coffee and Nuggets")
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
