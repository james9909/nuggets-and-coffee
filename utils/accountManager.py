import sqlite3, hashlib

def authenticate(g_username,g_password):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE username="+"'"+g_username+"'"+";")
    pass_hold = c.fetchall()

    worked = False
    message = ""

    db.commit()
    db.close()

    for line in pass_hold:
        for entry in line:
            if g_password == entry:
                worked = True
                message = "login info correct"
                return worked, message
            elif g_password != entry:
                message = "wrong password"
                return worked,message
    message = "user does not exist"
    return worked, message

def register(g_username,g_password,g_password2, g_type):    #user-username, password-password, pwd-retype

    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    worked = False
    message = ""

    checkUser = 'SELECT * FROM users WHERE username==?;'
    c.execute(checkUser, (g_username,))

    l = c.fetchone() #listifies the results

    if l != None:
        message = "username taken"
    elif g_password != g_password2:
        message = "passwords do not match"
    elif g_password == g_password2:
        c.execute('INSERT INTO users VALUES (NULL,?,?,?,"");', (g_username, g_password, g_type,))
        worked = True
        message = "user %s registered!" % (g_username)

    db.commit() #save changes
    db.close()  #close database

    return worked, message

def updateInfo(username, **kwargs):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    for k,v in kwargs.items():
        q = "UPDATE users SET %s=? WHERE username==?" % k
        c.execute(q, (v, username,))

    db.commit() #save changes
    db.close()  #close database

    return "updated"

def getInfo(username):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    q = "SELECT * FROM users WHERE username==?"

    c.execute(q, (username,))

    result = c.fetchone()

    return result

def get_type(username):
    f = "database.db"
    db = sqlite3.connect(f, check_same_thread=False)
    c = db.cursor()

    q = "SELECT type FROM users WHERE username==?"

    c.execute(q, (username,))

    result = c.fetchone()

    return result

#print(get_type("s"))
