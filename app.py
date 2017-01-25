import os
import random
from flask import Flask, render_template, session, redirect, url_for

import api
from utils import accountManager, config, db_builder, postManager

app = Flask(__name__)
app.register_blueprint(api.api, url_prefix="/api")

@app.route("/")
def index():
    if "username" in session:
        name = session["username"]
        _type=accountManager.get_type(name)[0]
        if _type == "coffee":
            return render_template("mainCoffee.html")
        elif _type == "nuggets":
            return render_template("mainNuggets.html")
        else:
            return render_template("main.html")
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
        return render_template("main.html", type=accountManager.get_type(session["username"][0]))
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

@app.route("/Nlocation")
def Nlocation():
    return render_template("Nlocation.html")

@app.route("/Clocation")
def Clocation():
    return render_template("Clocation.html")

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

@app.route("/createPost")
def createPost():
    return render_template("createPost.html")

@app.route("/recipes")
def show_recipes():
    return render_template("recipes.html", posted = "false", valueq="Coffee and Nuggets")

if __name__ == "__main__":
    db_builder.create_tables()

    # Generate and store secret key if it doesn't exist
    with open(".secret_key", "a+b") as f:
        secret_key = f.read()
        if not secret_key:
            secret_key = os.urandom(64)
            f.write(secret_key)
            f.flush()
        app.secret_key = secret_key

    config.load_keys()
    app.run()
