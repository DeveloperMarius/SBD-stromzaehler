from functools import wraps
from flask import request
from utils import get_jwt_from_request, is_jwt_in_request, is_body_signature_valid
from utils import Variables


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        jwt = get_jwt_from_request(request)
        if jwt is None:
            if is_jwt_in_request(request):
                message = 'Invalid Authentication Token'
            else:
                message = 'Authentication Token not provided'
            Variables.get_logger().log(request, message)
            return {
                "message": message,
                "data": None,
                "error": "Unauthorized"
            }, 401

        Variables.get_logger().log(request, 'Successfully authorized!')
        return f(jwt['id'], *args, **kwargs)

    return decorated
