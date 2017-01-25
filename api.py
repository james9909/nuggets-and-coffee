from flask import Blueprint, request, session

import hashlib

from decorators import api_wrapper
from utils import accountManager, postManager, apifunctions

api = Blueprint("api", __name__)

@api.route("/user/register", methods=["POST"])
@api_wrapper
def register():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["passconfirm"]

    success, message = accountManager.register(username, password, confirm_password)

    response = {"success": success, "message": message}

    if success:
        session["username"] = username
        response["redirect"] = "/"

    return response

@api.route("/user/login", methods=["POST"])
@api_wrapper
def login():
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = hashlib.sha1(password).hexdigest()

    success, message = accountManager.authenticate(username, hashed_password)

    response = {"success": success, "message": message}

    if success:
        session["username"] = username

    return response

@api.route("/user/updateType", methods=["POST"])
@api_wrapper
def update_type():
    _type = request.form["type"]
    accountManager.updateInfo(session.get("username"), type=_type)
    return {"success": 1, "message": "Preference set to %s" % _type}

@api.route("/post/create", methods=["POST"])
@api_wrapper
def create_post():
    username = session["username"]
    title = request.form["title"]
    content = request.form["content"]
    postid = postManager.createPost(username, title, content)

    response = {"success": 1, "redirect": "/forum/%s" % postid}

    return response

@api.route("/post/reply", methods=["POST"])
@api_wrapper
def reply():
    username = session.get("username", "anonymous")
    postid = request.form["postid"]
    content = request.form["content"]
    postManager.makeReply(username, postid, content)
    return {"success": 1, "redirect": "/forum/%s" % postid}

@api.route("/recipes", methods=["POST"])
@api_wrapper
def recipes():
    type_r = request.form["food_query"]
    recipes = apifunctions.get_recipes(type_r)
    if len(recipes) == 0:
        return {"success": 0, "message": "No recipes found."}

    r_images = apifunctions.get_image(recipes)
    r_titles = apifunctions.get_titles(recipes)
    r_urls = apifunctions.get_source(recipes)
    f_urls = apifunctions.get_f2f(recipes)
    r_rank = apifunctions.get_rank(recipes)
    p_ub = apifunctions.get_pub(recipes)
    p_url = apifunctions.get_puburl(recipes)
    return_recipes = []
    for x in range(len(r_images)):
        recipe = {
            "image": r_images[x],
            "title": r_titles[x],
            "recipeUrl": r_urls[x],
            "f2fUrl": f_urls[x],
            "ranking": r_rank[x],
            "publisher": p_ub[x],
            "publisherUrl": p_url[x]
        }
        return_recipes.append(recipe)
    return {"success": 1, "message": "Recipes found!", "recipes": return_recipes}

@api.route("/locations", methods=["POST"])
@api_wrapper
def locations():
    _type = request.form["type"]
    address = request.form["address"]
    coords = apifunctions.getlatlng(address)
    if len(coords) != 2:
        return {"success": 0, "message": "No locations found."}

    spots = apifunctions.foursq(coords[0], coords[1], _type)
    if len(spots) > 0:
        return {"success": 1, "message": "Locations found!", "locations": spots}
    return {"success": 0, "message": "No locations found."}
