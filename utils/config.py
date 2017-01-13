import os

def load_keys():
    global keys
    keys = {}

    if os.path.exists(".keys"):
        f = open(".keys", "r")
        for line in f:
            if "=" in line:
                line = line.split("=")
                key, value = line[0], line[1]
                keys[key] = value
