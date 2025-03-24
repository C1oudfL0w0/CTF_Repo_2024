#! /usr/bin/env python
# encoding=utf-8
from flask import Flask
from flask import request
import hashlib
import urllib.parse
import os
import json

app = Flask(__name__)

secret_key = os.urandom(16)


class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)
        if not os.path.exists(self.sandbox):
            os.mkdir(self.sandbox)

    def Exec(self):
        result = {}
        result['code'] = 500
        if self.checkSign():
            if "scan" in self.action:
                resp = scan(self.param)
                if resp == "Connection Timeout":
                    result['data'] = resp
                else:
                    print(resp)
                    self.append_to_file(resp)  # 追加内容到已存在的文件
                    result['code'] = 200
            if "read" in self.action:
                result['code'] = 200
                result['data'] = self.read_from_file()  # 从已存在的文件中读取
            if result['code'] == 500:
                result['data'] = "Action Error"
        else:
            result['code'] = 500
            result['msg'] = "Sign Error"
        return result

    def checkSign(self):
        if get_sign(self.action, self.param) == self.sign:
            return True
        else:
            return False


@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.parse.unquote(request.args.get("param", ""))
    action = "scan"
    return get_sign(action, param)


@app.route('/De1ta', methods=['GET', 'POST'])
def challenge():
    action = urllib.parse.unquote(request.cookies.get("action"))
    param = urllib.parse.unquote(request.args.get("param", ""))
    sign = urllib.parse.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
    if waf(param):
        return "No Hacker!!!!"
    task = Task(action, param, sign, ip)
    return json.dumps(task.Exec())


@app.route('/')
def index():
    return open("code.txt", "r").read()


def scan(param):
    try:
        with open(param, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file does not exist"


def md5(content):
    return hashlib.md5(content.encode()).hexdigest()


def get_sign(action, param):
    return hashlib.md5(secret_key + param.encode('latin1') + action.encode('latin1')).hexdigest()


def waf(param):
    check = param.strip().lower()
    if check.startswith("gopher") or check.startswith("file"):
        return True
    else:
        return False


if __name__ == '__main__':
    app.debug = False
    app.run()