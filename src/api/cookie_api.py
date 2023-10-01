import requests

COOKIE_URL = " "

def get_cookie():
    r = requests.get(COOKIE_URL, tineout=5)
    return r.json()["cookies"]