import sqlite3
import os


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(f"{os.path.dirname(os.path.realpath(__file__))}/../res/database.db", check_same_thread=False, isolation_level=None)
        self.connection.row_factory = Database.dict_factory
        self.cursor = self.connection.cursor()

    def clear_database(self):
        self.cursor.execute('DELETE FROM readings')
        self.cursor.execute('DELETE FROM logs')
        self.cursor.execute('DELETE FROM settings')

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d