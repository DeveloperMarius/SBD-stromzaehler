from datetime import datetime


class Logger:

    def __init__(self, database):
        self.database = database

    def log(self, request, message, jwt_id=None):
        data = (datetime.now(), request.path, request.method, jwt_id, message)
        self.database.cursor.execute('INSERT INTO logs ("timestamp", "endpoint", "method", "jwt_id", "message") VALUES (?, ?, ?, ?, ?)', data)
