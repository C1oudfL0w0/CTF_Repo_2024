import base64
import hashlib
import hmac
import pickle

from flask import make_response, request

unicode = str
basestring = str


# Quoted from python bottle template, thanks :D

def cookie_encode(data, key):
    msg = base64.b64encode(pickle.dumps(data, -1))
    sig = base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())
    return tob('!') + sig + tob('?') + msg


def cookie_decode(data, key):
    data = tob(data)
    if cookie_is_encoded(data):
        sig, msg = data.split(tob('?'), 1)
        if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())):
            return pickle.loads(base64.b64decode(msg))
    return None


def waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word in data:
            valid = True
            print(word)
            break
    return valid


def cookie_check(key, secret=None):
    a = request.cookies.get(key)
    data = tob(request.cookies.get(key))
    if data:
        if cookie_is_encoded(data):
            sig, msg = data.split(tob('?'), 1)
            if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(secret), msg, digestmod=hashlib.md5).digest())):
                res = base64.b64decode(msg)
                if waf(res):
                    return True
                else:
                    return False
        return True
    else:
        return False


def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)


def get_cookie(key, default=None, secret=None):
    value = request.cookies.get(key)
    if secret and value:
        dec = cookie_decode(value, secret)
        return dec[1] if dec and dec[0] == key else default
    return value or default


def cookie_is_encoded(data):
    print(data)
    return bool(data.startswith(tob('!')) and tob('?') in data)


def _lscmp(a, b):
    return not sum(0 if x == y else 1 for x, y in zip(a, b)) and len(a) == len(b)


def set_cookie(name, value, secret=None, **options):
    if secret:
        value = touni(cookie_encode((name, value), secret))
        resp = make_response("success")
        resp.set_cookie("user", value, max_age=3600)
        return resp
    elif not isinstance(value, basestring):
        raise TypeError('Secret key missing for non-string Cookie.')

    if len(value) > 4096:
        raise ValueError('Cookie value to long.')


def touni(s, enc='utf8', err='strict'):
    return s.decode(enc, err) if isinstance(s, bytes) else unicode(s)