from flask import make_response
from functools import wraps


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        r = make_response(fun(*args, **kwargs))
        r.headers['Access-Control-Allow-Origin'] = '*'
        r.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
        allow_headers = "Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type"
        r.headers['Access-Control-Allow-Headers'] = allow_headers
        return r

    return wrapper_fun
