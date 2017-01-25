from flask import make_response, redirect, session
from functools import wraps

import json
import traceback

response_header = { "Content-Type": "application/json; charset=utf-8" }

def api_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        web_result = {}
        response = 200
        try:
            web_result = f(*args, **kwargs)
        except Exception as error:
            traceback.print_exc()
            web_result = { "success": 0, "message": "Something went wrong!"}
        result = (json.dumps(web_result), response, response_header)
        response = make_response(result)

        return response
    return wrapper

def redirect_if_not_logged_in(route):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "username" not in session:
                return redirect(route)
            return f(*args, **kwargs)
        return wrapper
    return decorator
