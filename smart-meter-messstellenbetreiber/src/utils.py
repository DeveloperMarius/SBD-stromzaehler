import jwt
import os
from variables import Variables


def is_jwt_in_request(request):
    return "Authorization" in request.headers


def get_jwt_from_request(request):
    if not is_jwt_in_request(request):
        return None

    token = request.headers["Authorization"].split(" ")[1]
    jwt_data = jwt.decode(token, options={"verify_signature": False})

    if jwt_data is None or jwt_data['id'] is None:
        return None

    Variables.get_database().cursor.execute('SELECT secret_key FROM stromzaehler WHERE id=?', jwt_data['id'])
    secret_key_data = Variables.get_database().cursor.fetchone()

    if secret_key_data is None:
        return None

    try:
        data = jwt.decode(token, secret_key_data['secret_key'], algorithms=["HS256"])
        return data
    except Exception as e:
        print(str(e))
    return None
