from variables import Variables
import random
from utils import get_current_milliseconds
# import requests
import jwt
import os
# from dotenv import load_dotenv


class Stromzaehler:

    @staticmethod
    def simulate_energyusage():
        Variables.get_database().cursor.execute('SELECT value FROM zaehlerstand ORDER BY timestamp DESC LIMIT 1')
        last_value = Variables.get_database().cursor.fetchall()
        usage = random.randint(18, 28)

        if len(last_value) != 0:
            usage = usage + last_value[0]['value']

        Variables.get_database().cursor.execute('INSERT INTO zaehlerstand ("timestamp", "value") VALUES (?, ?)',
                                                (get_current_milliseconds(), usage))

    def send_data(self):
        Variables.get_database().cursor.execute('SELECT * FROM zaehlerstand')
        readings = Variables.get_database().cursor.fetchall()

        Variables.get_database().cursor.execute('SELECT * FROM logs')
        logs = Variables.get_database().cursor.fetchall()

        data = {
            'readings': readings,
            'logs': logs
        }
        jwt_token = jwt.encode(data, os.getenv("JWT_SECRET_KEY"), "HS256")


if __name__ == '__main__':
    # load_dotenv()
    print(f' jwt: {os.getenv("JWT_SECRET_KEY")}')
    Stromzaehler.simulate_energyusage()
