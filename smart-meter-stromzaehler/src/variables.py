from database import Database
from logger import Logger

db_instance = Database()
logger_instance = Logger(db_instance)


def get_logger():
    global logger_instance
    return logger_instance
