import sqlite3
import os


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/../res/stromzaehler.db", check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()
