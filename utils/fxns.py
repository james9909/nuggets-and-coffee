import sqlite3

db = sqlite3.connect("data/dab.db", check_same_thread=False)
d = db.cursor()

# =========== START ACCESSOR METHODS =============

def get_username(userid):
    q = 'SELECT username FROM users WHERE id =\"%s\";' % (userid)
    d.execute(q)
    r = d.fetchall()
    
    return r[0][0]

# ========== END ACCESSOR METHODS ================
