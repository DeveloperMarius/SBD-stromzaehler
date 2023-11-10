from utils import get_current_milliseconds
from datetime import datetime

class Logger:

    def __init__(self, database):
        self.database = database

    def log(self, message):
        timestamp = datetime.fromtimestamp(get_current_milliseconds() / 1000)
        self.database.cursor.execute('INSERT INTO logs ("timestamp", "message") VALUES (?, ?)', (timestamp, message))
