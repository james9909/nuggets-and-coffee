import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)
d = db.cursor()

def get_username(userid):
    q = 'SELECT username FROM users WHERE id =\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()

    return r[0][0]
