from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        result = run_cowsay(user_input)
    return render_template('index.html', result=result)

@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        user_input = request.form['user_input']
        result = run_cowsay(user_input)
    return render_template('index.html', result=result)

def run_cowsay(text):
    try:
        if waf(text):
            cmd_output = subprocess.check_output('cowsay ' + text, text=True, stderr=subprocess.STDOUT, shell=True)
            return cmd_output.strip()
        else:
            cmd_output = subprocess.check_output('cowsay Waf!', text=True, stderr=subprocess.STDOUT, shell=True)
            return cmd_output.strip()
    except subprocess.CalledProcessError as e:
        return run_cowsay("ERROR!")

def waf(string):
    blacklist = ['echo', 'cat', 'tee', ';', '|', '&', '<', '>', '\\', 'flag']
    for black in blacklist:
        if black in string:
            return False
    return True

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)