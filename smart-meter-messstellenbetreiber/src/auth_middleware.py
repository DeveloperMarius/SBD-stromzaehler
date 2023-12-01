from functools import wraps
from flask import request
from utils import get_jwt_from_request, is_jwt_in_request
from utils import Variables


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        message = ''

        jwt = get_jwt_from_request(request)
        if jwt is None:
            if is_jwt_in_request(request):
                Variables.get_logger().log(request, "Invalid Authentication Token!")
                message = 'Invalid Authentication Token'
            else:
                Variables.get_logger().log(request, "Authentication Token not provided!")
                message = 'Authentication Token not provided'
            return {
                "message": message,
                "data": None,
                "error": "Unauthorized"
            }, 401

        Variables.get_logger().log(request, 'Successfully authorized!')
        # return f(current_user, *args, **kwargs)
        return f(jwt['id'], *args, **kwargs)

    return decorated
