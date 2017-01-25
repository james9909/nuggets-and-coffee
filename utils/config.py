import os

def load_keys():
    global keys
    keys = {}

    if os.path.exists("utils/.keys"):
        f = open("utils/.keys", "r")
        for line in f:
            if "=" in line:
                line = line.strip().split("=")
                key, value = line[0], line[1]
                keys[key] = value
