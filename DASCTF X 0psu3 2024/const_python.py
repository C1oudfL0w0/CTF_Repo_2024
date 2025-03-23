import builtins
import io
import sys
import uuid
from flask import Flask, request, jsonify, session
import pickle
import base64

app = Flask(__name__)

app.config['SECRET_KEY'] = str(uuid.uuid4()).replace("-", "")


class User:

    def __init__(self, username, password, auth='ctfer'):
        self.username = username
        self.password = password
        self.auth = auth


password = str(uuid.uuid4()).replace("-", "")
Admin = User('admin', password, "admin")


@app.route('/')
def index():
    return "Welcome to my application"


@app.route('/login', methods=['GET', 'POST'])
def post_login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin':
            if password == admin.password:
                session['username'] = "admin"
                return "Welcome Admin"
            else:
                return "Invalid Credentials"
        else:
            session['username'] = username

    return '''
        <form method="post">
        <!-- /src may help you>
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/ppicklee', methods=['POST'])
def ppicklee():
    data = request.form['data']

    sys.modules['os'] = "not allowed"
    sys.modules['sys'] = "not allowed"
    # try:

    pickle_data = base64.b64decode(data)
    for i in {
            "os", "system", "eval", 'setstate', "globals", 'exec',
            '__builtins__', 'template', 'render', '\\', 'compile', 'requests',
            'exit', 'pickle', "class", "mro", "flask", "sys", "base", "init",
            "config", "session"
    }:
        if i.encode() in pickle_data:
            return i + " waf !!!!!!!"

    print(pickle.loads(pickle_data).read())
    return "success pickle"
    # except Exception as e:
    #     return "fail pickle"


@app.route('/admin', methods=['POST'])
def admin():
    username = session['username']
    if username != "admin":
        return jsonify({"message": 'You are not admin!'})
    return "Welcome Admin"


@app.route('/src')
def src():
    return open("app.py", "r", encoding="utf-8").read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
