import logging
import jwt
import os
import time
from models import Stromzaehler, Log, Kundenportal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from cryptography.hazmat.primitives import serialization
from flask import jsonify
import json
import hashlib
import sys
import traceback


def get_current_milliseconds():
    return round(time.time() * 1000)


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
        self.engine = create_engine(f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/../res/database.db", echo=False)

    def get_engin(self):
        return self.engine


class Logger:
    @staticmethod
    def log(request, message, source_type=None, source_id=None):
        logging.debug(f"{request.method} {request.path}: {message}")
        log = Log(
            timestamp=get_current_milliseconds(),
            endpoint=request.path,
            method=request.method,
            source_type=source_type,
            source_id=source_id,
            message=message
        )
        with Session(Variables.get_database().get_engin()) as session:
            session.add(log)
            session.commit()


def is_jwt_in_request(request):
    return "Authorization" in request.headers


def is_body_signature_valid(request, jwt_body) -> bool:
    if jwt_body['mode'] is None or jwt_body['mode'] != 'SHA256' or jwt_body['signature'] is None:
        return False
    body = request.get_json()
    actual_hash = hashlib.sha256(json.dumps(body).encode('utf-8')).hexdigest()
    return actual_hash == jwt_body['signature']


def get_jwt_from_request(request, entity_type):
    if not is_jwt_in_request(request):
        return None

    token = request.headers["Authorization"].split(" ")[1]
    jwt_data = jwt.decode(token, options={"verify_signature": False})

    if jwt_data is None or jwt_data['type'] is None or jwt_data['id'] is None:
        return None

    if entity_type == 'stromzaehler':
        if jwt_data['type'] == 'stromzaehler':
            statement = select(Stromzaehler.public_key).where(Stromzaehler.id == jwt_data['id'])

            with Session(Variables.get_database().get_engin()) as session:
                public_key = session.scalar(statement).replace('\\n', '\n')
        else:
            return None
    elif entity_type == 'kundenportal':
        if jwt_data['type'] == 'kundenportal':
            statement = select(Kundenportal.public_key).where(Kundenportal.id == jwt_data['id'])
            with Session(Variables.get_database().get_engin()) as session:
                public_key = session.scalar(statement).replace('\\n', '\n')
        else:
            return None
    else:
        return None

    if public_key is None:
        return None

    try:
        key = serialization.load_pem_public_key((public_key.encode()))
        data = jwt.decode(token, key, algorithms=['EdDSA'])
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f'{exc_type}: {str(e)} - {traceback.format_exc()}')
        return None

    if is_body_signature_valid(request, data):
        return data
    else:
        return None


def get_private_rsa_key():
    key = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
    private_key = serialization.load_pem_private_key((key.encode()), password=None)
    return private_key


def get_public_rsa_key():
    key = os.getenv('PUBLIC_KEY').replace('\\n', '\n')
    return str(key)


def signing_response(body: dict):
    response = jsonify(body)

    jwt_data = {
        'mode': "SHA256",
        'signature': hashlib.sha256(json.dumps(body).encode('utf-8')).hexdigest()
    }

    jwt_token = 'Bearer ' + jwt.encode(jwt_data, get_private_rsa_key(), "EdDSA", headers={'crv': 'Ed25519'})

    response.headers['Authorization'] = jwt_token

    return response
