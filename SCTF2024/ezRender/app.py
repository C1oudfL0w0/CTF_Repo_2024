from flask import Flask, render_template, request, render_template_string,redirect
from verify import *
from User import User
import base64
from waf import waf

app = Flask(__name__,static_folder="static",template_folder="templates")
user={}

@app.route('/register', methods=["POST","GET"])
def register():
    method=request.method
    if method=="GET":
        return render_template("register.html")
    if method=="POST":
        data = request.get_json()
        name = data["username"]
        pwd = data["password"]
        if name != None and pwd != None:
            if data["username"] in user:
                return "This name had been registered"
            else:
                user[name] = User(name, pwd)
                return "OK"

@app.route('/login', methods=["POST","GET"])
def login():
    method=request.method
    if method=="GET":
        return render_template("login.html")
    if method=="POST":
        data = request.get_json()
        name = data["username"]
        pwd = data["password"]
        if name != None and pwd != None:
            if name not in user:
                return "This account is not exist"
            else:
                if user[name].pwd == pwd:
                    token=generateToken(user[name])
                    return "OK",200,{"Set-Cookie":"Token="+token}
                else:
                    return "Wrong password"

@app.route('/admin', methods=["POST","GET"])
def admin():
    try:
        token = request.headers.get("Cookie")[6:]
    except:
        return "Please login first"
    else:
        infor = json.loads(base64.b64decode(token))
        name = infor["name"]
        token = infor["secret"]
        result = check(user[name], token)

    method=request.method
    if method=="GET":
        return render_template("admin.html",name=name)
    if method=="POST":
        template = request.form.get("code")
        if result != "True":
            return result, 401
        #just only blackList
        if waf(template):
            return "Hacker Found"
        result=render_template_string(template)
        print(result)
        if result !=None:
            return "OK"
        else:
            return "error"

@app.route('/', methods=["GET"])
def index():
    return redirect("login")

@app.route('/removeUser', methods=["POST"])
def remove():
    try:
        token = request.headers.get("Cookie")[6:]
    except:
        return "Please login first"
    else:
        infor = json.loads(base64.b64decode(token))
        name = infor["name"]
        token = infor["secret"]
        result = check(user[name], token)
    if result != "True":
        return result, 401

    rmuser=request.form.get("username")
    user.pop(rmuser)
    return "Successfully Removed:"+rmuser

if __name__ == '__main__':
    # for the safe
    del __builtins__.__dict__['eval']
    app.run(debug=False, host='0.0.0.0', port=8081)