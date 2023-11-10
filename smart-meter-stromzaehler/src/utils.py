import jwt
import os
import time


def is_jwt_in_request(request):
    return "Authorization" in request.headers


def get_jwt_from_request(request):
    if not is_jwt_in_request(request):
        return None
    token = request.headers["Authorization"].split(" ")[1]
    try:
        data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        return data
    except Exception as e:
        print(str(e))
    return None


def get_current_milliseconds():
    return round(time.time() * 1000)