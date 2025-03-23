from sanic import Sanic
from sanic.response import json,file as file_,text,redirect
from sanic_cors import CORS
from key import secret_key
import os
import pickle
import time
import jwt
import io
import builtins
app = Sanic("App")
pickle_file = "data.pkl"
my_object = {}
users = []

safe_modules = {
    'math',
    'datetime',
    'json',
    'collections',
}

safe_names = {
    'sqrt', 'pow', 'sin', 'cos', 'tan',
    'date', 'datetime', 'timedelta', 'timezone', 
    'loads', 'dumps',  
    'namedtuple', 'deque', 'Counter', 'defaultdict'
}

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module in safe_modules and name in safe_names:
            print(getattr(builtins, name))
            return getattr(builtins, name)
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %(module, name))
    
def restricted_loads(s):
    return RestrictedUnpickler(io.BytesIO(s)).load()

CORS(app, supports_credentials=True, origins=["http://localhost:8000", "http://127.0.0.1:8000"])
class User:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        

def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

def token_required(func):
    async def wrapper(request, *args, **kwargs):
        token = request.cookies.get("token")  
        if not token:
            return redirect('/login')
        try:
            result=jwt.decode(token, str(secret_key), algorithms=['HS256'], options={"verify_signature": True})
        except jwt.ExpiredSignatureError:
            return json({"status": "fail", "message": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return json({"status": "fail", "message": "Invalid token"}, status=401)
        print(result)
        if result["role"]!="admin":
            return json({"status": "fail", "message": "Permission Denied"}, status=401)
        return await func(request, *args, **kwargs)
    return wrapper

@app.route('/', methods=["GET"])
def file_reader(request):
    file = "app.py"
    with open(file, 'r') as f:
        content = f.read()
    return text(content)

@app.route('/upload', methods=["GET","POST"])
# @token_required
async def upload(request):
    if request.method=="GET":
        return await file_('templates/upload.html')
    if not request.files:
        return text("No file provided", status=400)

    file = request.files.get('file')
    file_object = file[0] if isinstance(file, list) else file
    print(file_object.body)

    # try:
    new_data = restricted_loads(file_object.body)
        # try:
            # my_object.update(new_data)
        # except:
        #     return json({"status": "success", "message": "Pickle object loaded but not updated"})
        # with open(pickle_file, "wb") as f:
        #     pickle.dump(my_object, f)

    return json({"status": "success", "message": "Pickle object updated"})
    # except pickle.UnpicklingError:
    #     return text("Dangerous pickle file", status=400)
    
@app.route('/register', methods=['GET','POST'])
async def register(request):
    if request.method=='GET':
        return await file_('templates/register.html')
    if request.json:
        NewUser=User("username","password")
        merge(request.json, NewUser)
        users.append(NewUser)
    else:
        return json({"status": "fail", "message": "Invalid request"}, status=400)
    return json({"status": "success", "message": "Register Success!","redirect": "/login"})

@app.route('/login', methods=['GET','POST'])
async def login(request):
    if request.method=='GET':
        return await file_('templates/login.html')
    if request.json:
        username = request.json.get("username")
        password = request.json.get("password")
        if not username or not password:
            return json({"status": "fail", "message": "Username or password missing"}, status=400)
        user = next((u for u in users if u.username == username), None)
        if user:
            if user.password == password:
                data={"user":username,"role":"guest"}
                data['exp'] = int(time.time()) + 60 *5
                token = jwt.encode(data, str(secret_key), algorithm='HS256')
                response = json({"status": "success", "redirect": "/upload"})
                response.cookies["token"]=token
                response.headers['Access-Control-Allow-Origin'] = request.headers.get('origin')
                return response
            else:
                return json({"status": "fail", "message": "Invalid password"}, status=400)
        else:
            return json({"status": "fail", "message": "User not found"}, status=404)
    return json({"status": "fail", "message": "Invalid request"}, status=400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)