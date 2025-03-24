from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

@app.route('/')
def inedx():
    name = request.args.get("name","")
    if name == "":
        return redirect("/?name=hello")
    return render_template_string(name)

app.run("0.0.0.0", port=8080)