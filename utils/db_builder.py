import sqlite3

DATABASE = "database.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, type TEXT, location INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS posts (username TEXT, postid INTEGER PRIMARY KEY, title TEXT, content TEXT, timestamp INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS replies (username TEXT, postid INTEGER, content TEXT, timestamp INTEGER)")

    db.commit()
    db.close()
