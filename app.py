import hashlib, os, json, random
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for
import urllib, math, sys
from itertools import count, groupby

app = Flask(__name__)

app.secret_key = os.urandom(32)
secret = 'secret_cookie_key'

#========================================ROUTAGE

#either shows user their home (stories edited by them), or redirect to login
@app.route("/")
def index():
    if (secret in session):
        name = session[secret]
        return render_template('index.html')
    return render_template('base.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
