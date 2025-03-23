import json
import hashlib
import base64
import jwt
from app import *
from User import *
def check(user,crypt):
    verify_c=crypt
    secret_key = user.secret
    try:
        decrypt_infor = jwt.decode(verify_c, secret_key, algorithms=['HS256'])
        if decrypt_infor["is_admin"]=="1":
            return "True"
        else:
            return "You r not admin"
    except:
        return 'Don\'t be a Hacker!!!'

def generateToken(user):
    secret_key=user.secret
    secret={"name":user.name,"is_admin":"0"}

    verify_c=jwt.encode(secret, secret_key, algorithm='HS256')
    infor={"name":user.name,"secret":verify_c}
    token=base64.b64encode(json.dumps(infor).encode()).decode()
    return token
