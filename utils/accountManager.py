import hashlib
import sqlite3

def authenticate(username, password):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    success = False
    message = ""

    if result:
        print password
        print result[0]
        if result[0] == password:
            success = True
            message = "Success!"
        else:
            message = "Incorrect password"
    else:
        message = "User does not exist"

    db.close()
    return success, message

def register(username, password, password2, _type):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    success = False
    message = ""

    c.execute("SELECT * FROM users where username = ?", (username,))

    result = c.fetchone()

    if result:
        message = "Username taken"
    elif password != password2:
        message = "Passwords do not match"
    else:
        password = hashlib.sha1(password).hexdigest()
        c.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, '')", (username, password, _type,))
        success = True
        message = "Account created"

    db.commit()
    db.close()

    return success, message

def updateInfo(username, **kwargs):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    for k,v in kwargs.items():
        q = "UPDATE users SET %s = ? WHERE username = ?" % k
        c.execute(q, (v, username,))

    db.commit()
    db.close()

    return "Information updated"

def getInfo(username):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    q = "SELECT * FROM users WHERE username = ?"
    c.execute(q, (username,))
    result = c.fetchone()

    return result

def get_type(username):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    q = "SELECT type FROM users WHERE username = ?"

    c.execute(q, (username,))

    result = c.fetchone()

    return result
