import sqlite3


def authenticate(username,password):

    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok
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
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok

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
        message = "user %s registered!" % (user)

    db.commit() #save changes
    db.close()  #close database
    return worked, message

