from database import Database
from logger import Logger


class Variables:
    db_instance = None
    logger_instance = None

    @staticmethod
    def get_logger():
        if Variables.logger_instance is None:
            Variables.logger_instance = Logger(Variables.get_database())
        return Variables.logger_instance

    @staticmethod
    def get_database(database_location=None):
        if Variables.db_instance is None:
            Variables.db_instance = Database(database_location)
        return Variables.db_instance
