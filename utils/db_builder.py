import sqlite3

DATABASE = "data.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, type TEXT, location INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT, userid INTEGER, timestamp INTEGER, content TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS replies (id INTEGER PRIMARY KEY, postid INTEGER, userid INTEGER, timestamp INTEGER, content TEXT)")

    db.commit()
    db.close()
