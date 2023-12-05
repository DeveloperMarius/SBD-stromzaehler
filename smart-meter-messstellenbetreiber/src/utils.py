import jwt
import os
from models import Stromzaehler, Log, Kundenportal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from cryptography.hazmat.primitives import serialization
from flask import jsonify
import json
import hashlib


class Variables:
    db_instance = None
    logger_instance = None

    @staticmethod
    def get_logger():
        if Variables.logger_instance is None:
            Variables.logger_instance = Logger()
        return Variables.logger_instance

    @staticmethod
    def get_database():
        if Variables.db_instance is None:
            Variables.db_instance = Database()
        return Variables.db_instance


class Database:

    def __init__(self):
        print(f"sqlite://{os.path.dirname(os.path.realpath(__file__))}/../res/messstellenbetreiber.db")
        engine = create_engine(f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/../res/messstellenbetreiber.db", echo=True)
        self.session = Session(engine)


class Logger:
    @staticmethod
    def log(request, message, jwt_id=None):
        print(f"{request.method} {request.path}: {message}")
        # data = (datetime.now(), request.path, request.method, jwt_id, message)
        # self.database.cursor.execute('INSERT INTO logs ("timestamp", "endpoint", "method", "jwt_id", "message") VALUES (?, ?, ?, ?, ?)', data)
        log = Log(
            timestamp=datetime.now(),
            endpoint=request.path,
            method=request.method,
            jwt_id=jwt_id,
            message=message
        )
        Variables.get_database().session.add(log)

        Variables.get_database().session.commit()


def is_jwt_in_request(request):
    return "Authorization" in request.headers


def is_body_signature_valid(request, jwt_body) -> bool:
    if jwt_body['mode'] is None or jwt_body['mode'] != 'SHA256' or jwt_body['signature'] is None:
        return False
    body = request.get_json()
    actual_hash = hashlib.sha256(json.dumps(body).encode('utf-8')).hexdigest()
    return actual_hash == jwt_body['signature']


def get_jwt_from_request(request):
    if not is_jwt_in_request(request):
        return None

    token = request.headers["Authorization"].split(" ")[1]
    jwt_data = jwt.decode(token, options={"verify_signature": False})

    if jwt_data is None or jwt_data['type'] is None or jwt_data['id'] is None:
        return None

    if jwt_data['type'] == 'stromzaehler':
        statement = select(Stromzaehler.public_key).where(Stromzaehler.id == jwt_data['id'])
        public_key = Variables.get_database().session.scalar(statement)
    elif jwt_data['type'] == 'kundenportal':
        statement = select(Kundenportal.public_key).where(Kundenportal.id == jwt_data['id'])
        public_key = Variables.get_database().session.scalar(statement)
    else:
        return None

    if public_key is None:
        return None

    try:
        key = serialization.load_ssh_public_key((public_key.encode()))
        data = jwt.decode(token, key, algorithms=['RS256'])
    except Exception as e:
        print(str(e))
        return None

    if is_body_signature_valid(request, data):
        return data
    else:
        return None


def get_private_rsa_key():
    with open('../res/id_rsa') as file:
        key = file.read()
    private_key = serialization.load_ssh_private_key((key.encode()), password=b'')
    return private_key


def get_public_rsa_key():
    with open('../res/id_rsa.pub') as file:
        key = file.read()
    return str(key)


def signing_response(body: dict):
    response = jsonify(body)

    jwt_data = {
        'mode': "SHA256",
        'signature': hashlib.sha256(json.dumps(body).encode('utf-8')).hexdigest()
    }

    jwt_token = 'Bearer ' + jwt.encode(jwt_data, get_private_rsa_key(), "RS256")

    response.headers['Authorization'] = jwt_token

    return response
