import sqlite3
import datetime

def getPost(postid):
    f = "database.db"
    db = sqlie3.connect(f)
    c = db.cursor()

    query = "SELECT * FROM posts WHERE postid==?"
    c.execute(query, (postid,))
    postinfo = c.fetchone()

    db.commit()
    db.close()
    return psotinfo

def createPost(username, title, content):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "INSERT INTO posts VALUES (?, NULL, ?, ?, ?)"

    timestamp = int(datetime.datetime.now().strftime("%s"))
    c.execute(query, (username, title, content, timestamp,))

  
    db.commit()
    db.close()
    return "created"

def makeReply(username, postid, content):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "INSERT INTO replies VALUES(?, ?, ?, ?)"

    timestamp = int(datetime.datetime.now().strftime("%s"))
    c.execute(query, (username, postid, content, timestamp,))

    db.commit()
    db.close()

def checkid(postid):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "SELECT * FROM posts WHERE postid==?"
    c.execute(query, (postid,))

    post = c.fetchone()

    return post != None
    
def getReplies(postid):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "SELECT * FROM replies WHERE postid==?"

    c.execute(query, (postid,))

    replies = c.fetchall()

    db.commit()
    db.close()

    return replies

def getPosts(**kwargs):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    if 'username' in kwargs:
        query = "SELECT * FROM posts WHERE username==?"
        c.execute(query, (username,))
    else:
        query = "SELECT * FROM posts"
        c.execute(query)
    

    posts = c.fetchall()

    db.commit()
    db.close()

    return posts
