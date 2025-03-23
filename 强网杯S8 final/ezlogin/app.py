from flask import Flask, request, render_template, redirect
from dataclasses import dataclass
from time import time
import jsonpickle
import base64
import json
import os

@dataclass
class User:
    username: str
    password: str

@dataclass
class Token:
    username: str
    timestamp: int

app = Flask(__name__)
users = [User('admin', os.urandom(32).hex()), User('guest', 'guest')]
BLACKLIST = [
    'repr',
    'state',
    'json',
    'reduce',
    'tuple',
    'nt',
    '\\',
    'builtins',
    'os',
    'popen',
    'exec',
    'eval',
    'posix', 
    'spawn',
    'compile',
    'code'
]

def waf(jtoken):
    otoken = json.loads(jtoken)
    token = json.dumps(otoken, ensure_ascii=False)
    for keyword in BLACKLIST:
        if keyword in token:
            return False
    return True
    

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    for user in users:
        if user.username == username and user.password == password:
            res = app.make_response('Login successful')
            token = Token(username, time())
            res.status_code = 302
            res.set_cookie('token', base64.urlsafe_b64encode(jsonpickle.encode(token).encode()).decode())
            res.headers['Location'] = '/home'
            return res

    return 'Invalid credentials (guest/guest)'

@app.route('/home')
def home():
    token = request.cookies.get('token')
    if token:
        jtoken = base64.urlsafe_b64decode(token.encode()).decode()
        if not waf(jtoken):
            return 'Invalid token'
        token = jsonpickle.decode(jtoken, safe=True)
        # if time() - token.timestamp < 60:
        #     if token.username != 'admin':
        #         return f'Welcome {token.username}, but you are not admin'
        #     return 'Welcome admin, there is something in /s3Cr3T'
    return 'Invalid token(1)'

@app.route('/s3Cr3T')
def secret():
    token = request.cookies.get('token')
    if token:
        jtoken = base64.urlsafe_b64decode(token.encode()).decode()
        if not waf(jtoken):
            return 'Invalid token'
        token = jsonpickle.decode(jtoken, safe=True)
        if time() - token.timestamp < 60:
            if token.username != 'admin':
                return 'Invalid token'
            return '''
if not waf(token):
    return 'Invalid token'
token = jsonpickle.decode(token, safe=True)
if time() - token.timestamp < 60:
    if token.username != 'admin':
        return f'Welcome {token.username}, but you are not admin'
    return 'Welcome admin, there is something in /s3Cr3T'
return 'Invalid token'
'''.strip()
    return 'Invalid token'

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)