import os

def load_keys():
    global keys
    keys = {}

    # Backwards compatibility
    if os.path.exists("utils/.keys"):
        f = open("utils/.keys", "r")
        for line in f:
            if "=" in line:
                line = line.strip().split("=")
                key, value = line[0], line[1]
                print "Loading key \"%s\"..." % key
                keys[key] = value

    if os.path.exists(".keys"):
        f = open(".keys", "r")
        for line in f:
            if "=" in line:
                line = line.strip().split("=")
                key, value = line[0], line[1]
                print "Loading key \"%s\"..." % key
                keys[key] = value
