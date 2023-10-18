import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect('../res/stromzaehler.db', check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()
