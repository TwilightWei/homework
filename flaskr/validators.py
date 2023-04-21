from functools import wraps
from flask import request, make_response
import jsonschema
from jsonschema import validate


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except jsonschema.exceptions.ValidationError as error:
            return make_response({
                'success': False,
                'message': 'Incorrect input format.'
            }, 400)
        return f(*args, **kw)
    return wrapper


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, schema)
            except jsonschema.exceptions.ValidationError as error:
                return make_response({
                'success': False,
                'message': 'Incorrect input format.'
            }, 400)
            return f(*args, **kw)
        return wrapper
    return decorator