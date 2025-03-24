from flask import *
import io
import os

app = Flask(__name__)
black_list = [
    '__build_class__', '__debug__', '__doc__', '__import__', 
    '__loader__', '__name__', '__package__', '__spec__', 'SystemExit',
    'breakpoint', 'compile', 'exit', 'memoryview', 'open', 'quit', 'input'
]
new_builtins = dict([
    (key, val) for key, val in __builtins__.__dict__.items() if key not in black_list
])

flag = "flag{xxxxxxxxx}"

@app.route("/")
def index():
    return redirect("/static/index.html")

@app.post("/run")
def run():
    out = io.StringIO()
    script = str(request.form["script"])
    
    def wrap_print(*args, **kwargs):
        kwargs["file"] = out
        print(*args, **kwargs)
    new_builtins["print"] = wrap_print

    try:
        exec(script, {"__builtins__": new_builtins})
    except Exception as e:
        wrap_print(e)
    
    ret = out.getvalue()
    out.close()
    return ret

app.run('0.0.0.0', port=9001)
