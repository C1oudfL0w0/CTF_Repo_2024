evilcode=["\\",
          "{%",
          "config",
          "session",
          "request",
          "self",
          "url_for",
          "current_app",
          "get_flashed_messages",
          "lipsum",
          "cycler",
          "joiner",
          "namespace",
          "chr",
          "request.",
          "|",
          "%c",
          "eval",
          "[",
          "]",
          "exec",
          "pop(",
          "get(",
          "setdefault",
          "getattr",
          ":",
          "os",
          "app"]
whiteList=[]
def waf(s):
    s=str(s.encode())[2:-1].replace("\\'","'").replace(" ","")
    if not s.isascii():
        return False
    else:
        for key in evilcode:
            if key in s:
                return True
    return False
