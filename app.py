import os
import random
from flask import Flask, render_template, session, redirect, url_for

import api
from decorators import login_required
from utils import accountManager, config, db_builder, postManager

app = Flask(__name__)
app.register_blueprint(api.api, url_prefix="/api")

@app.route("/")
@login_required
def index():
    name = session["username"]
    _type=accountManager.get_type(name)[0]
    if _type == "coffee":
        return render_template("mainCoffee.html")
    elif _type == "nuggets":
        return render_template("mainNuggets.html")
    else:
        # User hasn't set their preference yet
        return render_template("main.html")

@app.route("/login")
def login():
    with open('pics.txt', 'r') as myfile:
        data=myfile.read().strip().split(",")
    random.shuffle(data)

    return render_template("login.html", nc=data[:12])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register")
def create_account():
    with open('pics.txt', 'r') as myfile:
        data=myfile.read().strip().split(",")
    random.shuffle(data)

    return render_template("register.html", nc=data[:12])

@app.route("/favorites")
@login_required
def fav_page():
    return render_template("main.html", type=accountManager.get_type(session["username"][0]))

@app.route("/mainNuggets")
@login_required
def main_nug():
    return render_template("mainNuggets.html")

@app.route("/mainCoffee")
@login_required
def main_coffee():
    return render_template("mainCoffee.html")

@app.route("/Nlocation")
@login_required
def Nlocation():
    return render_template("Nlocation.html")

@app.route("/Clocation")
@login_required
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
@login_required
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
    app.debug = True
    app.run()
