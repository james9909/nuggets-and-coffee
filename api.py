from flask import Blueprint, request, session

import hashlib

from decorators import api_wrapper, WebException
from utils import accountManager, postManager

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
