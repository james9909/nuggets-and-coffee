import sqlite3
from hashlib import sha1


def authenticate(username,password):

    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops 
    worked = False
    message = ""
    passHash = sha1(password).hexdigest()#hash it

    checkUser = 'SELECT * FROM users WHERE username==?;'
    c.execute(checkUser, (username,))
    l = c.fetchone() #listifies the results
    if l == None:
        message = "user does not exist"
    elif l[1] == passHash:
        worked = True
        message = "login info correct"
    else:
        message = "wrong password"

    db.commit() #save changes
    db.close()  #close database
    return worked, message


def register(username,password,pwd):    #user-username, password-password, pwd-retype
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    worked = False
    message = ""


    checkUser = 'SELECT * FROM users WHERE username==?;'
    c.execute(checkUser, (username,))
    l = c.fetchone() #listifies the results

    if l != None:
        message = "username taken"
    elif (password != pwd):
        message = "passwords do not match"
    elif (password == pwd):
        passHash = sha1(password).hexdigest()#hash it
        insertUser = 'INSERT INTO users VALUES (NULL,?,?, "","");'

        c.execute(insertUser, (username, passHash,))

        worked = True
        message = "user %s registered!" % (username)

    db.commit() #save changes
    db.close()  #close database
    return worked, message

def updateInfo(username, **kwargs):
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops

    for k,v in kwargs.items():
        q = "UPDATE users SET %s=? WHERE username==?" % k
        c.execute(q, (v, username,))

    db.commit()
    db.close()
    return "updated"

def getInfo(username):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    q = "SELECT * FROM users WHERE username==?"

    c.execute(q, (username,))

    result = c.fetchone()

    db.commit()
    db.close()

    return result
