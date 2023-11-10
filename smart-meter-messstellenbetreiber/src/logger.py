from datetime import datetime
from utils import get_jwt_from_request

class Logger:

    def __init__(self, database):
        self.database = database

    def log(self, request, message):
        jwt = get_jwt_from_request(request)
        jwt_id = None
        if jwt is not None:
            jwt_id = jwt['jwt_id']

        data = (datetime.now(), request.path, request.method, jwt_id, message)
        self.database.cursor.execute('INSERT INTO logs ("timestamp", "endpoint", "method", "jwt_id", "message") VALUES (?, ?, ?, ?, ?)', data)
