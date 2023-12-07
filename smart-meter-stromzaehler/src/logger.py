from utils import get_current_milliseconds
from datetime import datetime
import logging


class Logger:

    def __init__(self, database):
        self.database = database

    def log(self, message):
        logging.debug(message)
        print(message)
        timestamp = datetime.fromtimestamp(get_current_milliseconds() / 1000)
        self.database.cursor.execute('INSERT INTO logs ("timestamp", "message") VALUES (?, ?)', (timestamp, message))
