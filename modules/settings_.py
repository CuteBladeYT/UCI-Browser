import json

SETTINGS = {}

def check():
    _sf = open("settings.json")
    SETTINGS = json.loads(_sf.read())
    _sf.close()
    return SETTINGS


def load():
    return SETTINGS