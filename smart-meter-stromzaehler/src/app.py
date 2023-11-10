from variables import Variables
import random
from utils import get_current_milliseconds
import requests
import jwt
import os
from dotenv import load_dotenv
import json
import hashlib
import hmac


class Stromzaehler:

    @staticmethod
    def simulate_energyusage():
        Variables.get_database().cursor.execute('SELECT value FROM readings ORDER BY timestamp DESC LIMIT 1')
        last_value = Variables.get_database().cursor.fetchall()
        usage = random.randint(18, 28)

        if len(last_value) != 0:
            usage = usage + last_value[0]['value']

        Variables.get_database().cursor.execute('INSERT INTO readings ("timestamp", "value") VALUES (?, ?)',
                                                (get_current_milliseconds(), usage))

    @staticmethod
    def send_data():
        Variables.get_database().cursor.execute('SELECT * FROM readings')
        readings = Variables.get_database().cursor.fetchall()

        Variables.get_database().cursor.execute('SELECT * FROM logs')
        logs = Variables.get_database().cursor.fetchall()

        body = json.dumps({
            'readings': readings,
            'logs': logs
        })

        jwt_data = {
            'id': os.getenv('STROMZAEHLER_ID'),
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }

        jwt_token = 'Bearer' + jwt.encode(jwt_data, os.getenv("JWT_SECRET_KEY"), "HS256")
        response = requests.post('http://localhost:3000', headers={'Authorization': jwt_token}, data=body)

        if response.status_code != 200:
            return
        Variables.get_database().cursor.execute('DELETE FROM readings ORDER BY timestamp DESC LIMIT -1 OFFSET 1')
        Variables.get_database().cursor.execute('DELETE FROM logs')


if __name__ == '__main__':
    load_dotenv()
    try:
        Stromzaehler.simulate_energyusage()
        Variables.get_logger().log('Successfully simulated energyusage!')
    except Exception as e:
        Variables.get_logger().log(f'Simulating energyusage failed! Fehler: {e}')

    try:
        Stromzaehler.send_data()
        Variables.get_logger().log('Successfully send data to Messstellenbetreiber.')
    except Exception as e:
        Variables.get_logger().log(f'Sending data to Messstellenbetreiber failed! Fehler: {e}')
