import jwt
import os
from models import Stromzaehler, Log
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select


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
        # data = (datetime.now(), request.path, request.method, jwt_id, message)
        # self.database.cursor.execute('INSERT INTO logs ("timestamp", "endpoint", "method", "jwt_id", "message") VALUES (?, ?, ?, ?, ?)', data)
        log = Log(
            timestamp=datetime.now(),
            enpoint=request.path,
            method=request.method,
            jwt_id=jwt_id,
            message=message
        )
        Variables.get_database().session.add(log)

        Variables.get_database().session.commit()


def is_jwt_in_request(request):
    return "Authorization" in request.headers


def get_jwt_from_request(request):
    if not is_jwt_in_request(request):
        return None

    token = request.headers["Authorization"].split(" ")[1]
    jwt_data = jwt.decode(token, options={"verify_signature": False})

    if jwt_data is None or jwt_data['id'] is None:
        return None

    statement = select(Stromzaehler.secret_key).where(Stromzaehler.id == jwt_data['id'])
    secret_key_data = Variables.get_database().session.scalar(statement)

    # Variables.get_database().cursor.execute('SELECT secret_key FROM stromzaehler WHERE id=?', jwt_data['id'])
    # secret_key_data = Variables.get_database().cursor.fetchone()

    if secret_key_data is None:
        return None

    try:
        data = jwt.decode(token, secret_key_data['secret_key'], algorithms=["HS256"])
        return data
    except Exception as e:
        print(str(e))
    return None
