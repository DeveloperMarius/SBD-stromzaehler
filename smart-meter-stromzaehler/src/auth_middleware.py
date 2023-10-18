from functools import wraps
from flask import request
from utils import get_jwt_from_request, is_jwt_in_request
from variables import get_logger


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        data = get_jwt_from_request(request)
        if data is None:
            if is_jwt_in_request(request):
                get_logger().log(request, "Invalid Authentication Token!")
            else:
                get_logger().log(request, "Authentication Token not provided!")
            return {
                "message": "Invalid Authentication Token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        get_logger().log(request, 'Successfully authorized!')
        # return f(current_user, *args, **kwargs)
        return f(*args, **kwargs)

    return decorated
