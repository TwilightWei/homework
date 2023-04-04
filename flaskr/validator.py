from functools import wraps
from flask import request, make_response
from jsonschema import validate


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except :
            return make_response({'message': 'Failed'}, 400)
        return f(*args, **kw)
    return wrapper


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, schema)
            except:
                return make_response({'message': 'Failed'}, 400)
            return f(*args, **kw)
        return wrapper
    return decorator