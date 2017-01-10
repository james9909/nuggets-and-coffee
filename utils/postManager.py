import sqlite3

def createPost(username, title, content):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "INSERT INTO posts VALUES (?, NULL, ?, ?, ?)"

    timestamp = int(datetime.datetime.now().strftime("%s"))
    c.execute(query, (username, title, content, timestamp,))

    db.commit()
    db.close()

def makeReply(username, postid, content):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "INSERT INTO replies VALUES(?, ?, ?, ?)"

    timestamp = int(datetime.datetime.now().strftime("%s"))
    c.execute(query, (username, postid, content, timestamp,))

    db.commit()
    db.close()


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
        query = "SELECT * FROM replies WHERE username==?"
        c.execute(query, (username,))
    else:
        query = "SELECT * FROM replies"
        c.execute(query)
    

    posts = c.fetchall()

    db.commit()
    db.close()

    return posts
