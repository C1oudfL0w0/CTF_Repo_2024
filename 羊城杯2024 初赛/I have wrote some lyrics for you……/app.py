import os
import random

from config.secret_key import secret_code
from flask import Flask, make_response, request, render_template
from cookie import set_cookie, cookie_check, get_cookie
import pickle

app = Flask(__name__)
app.secret_key = random.randbytes(16)


class UserData:
    def __init__(self, username):
        self.username = username


def Waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word.lower() in data.lower():
            valid = True
            break
    return valid


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/lyrics", methods=['GET'])
def lyrics():
    resp = make_response()
    resp.headers["Content-Type"] = 'text/plain; charset=UTF-8'
    query = request.args.get("lyrics")
    path = os.path.join(os.getcwd() + "/lyrics", query)

    try:
        with open(path) as f:
            res = f.read()
    except Exception as e:
        return "No lyrics found"
    return res


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        user = UserData(username)
        res = {"username": user.username}
        return set_cookie("user", res, secret=secret_code)
    return render_template('login.html')


@app.route("/board", methods=['GET'])
def board():
    invalid = cookie_check("user", secret=secret_code)
    if invalid:
        return "Nope, invalid code get out!"

    data = get_cookie("user", secret=secret_code)

    if isinstance(data, bytes):
        a = pickle.loads(data)
        data = str(data, encoding="utf-8")

    if "username" not in data:
        return render_template('user.html', name="guest")
    if data["username"] == "admin":
        return render_template('admin.html', name=data["username"])
    if data["username"] != "admin":
        return render_template('user.html', name=data["username"])


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    app.run(host="0.0.0.0", port=8081)