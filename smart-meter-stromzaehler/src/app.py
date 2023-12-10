from variables import Variables
import random
from utils import get_current_milliseconds
import requests
import jwt
import os
from dotenv import load_dotenv
import json
import hashlib
from cryptography.hazmat.primitives import serialization
import sys
import traceback


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
            'type': 'stromzaehler',
            'id': int(os.getenv('STROMZAEHLER_ID')),
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }

        key = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
        private_key = serialization.load_pem_private_key(key.encode(), password=None)

        jwt_token = 'Bearer ' + jwt.encode(jwt_data, private_key, "EdDSA", headers={'crv': 'Ed25519'})
        response = requests.post(os.getenv('MESSSTELLENBETREIBER_URL') + '/api/stromzaehler/update', headers={'Authorization': jwt_token, 'Content-Type': 'application/json'}, data=body)

        if response.status_code != 200:
            print(os.getenv('MESSSTELLENBETREIBER_URL'))
            Variables.get_logger().log('Server not available.')
            return

        if 'Authorization' not in response.headers:
            Variables.get_logger().log('JWT is not set in response.')
            return

        token = response.headers["Authorization"].split(" ")[-1]

        jwt_body = None
        try:
            key = serialization.load_pem_public_key((os.getenv('MESSSTELLENBETREIBER_PUBLIC_KEY').replace('\\n', '\n').encode()))
            jwt_body = jwt.decode(token, key, algorithms=['EdDSA'])
        except Exception as e:
            Variables.get_logger().log('JWT is invalid.')
            return

        if jwt_body['mode'] is None or jwt_body['mode'] != 'SHA256' or jwt_body['signature'] is None:
            Variables.get_logger().log('Signature or Mode not set.')
            return

        actual_hash = hashlib.sha256(json.dumps(response.json()).encode('utf-8')).hexdigest()
        if actual_hash != jwt_body['signature']:
            Variables.get_logger().log('Signature is invalid.')
            return

        Variables.get_database().cursor.execute('DELETE FROM readings ORDER BY timestamp LIMIT (SELECT COUNT(*) FROM readings)-1;')
        Variables.get_database().cursor.execute('DELETE FROM logs')
        Variables.get_logger().log('Data successfully sent to server.')


if __name__ == '__main__':
    load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")
    try:
        Stromzaehler.simulate_energyusage()
        Variables.get_logger().log('Successfully simulated energyusage!')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        Variables.get_logger().log(f'Simulating energyusage failed! Fehler: {exc_type}: {str(e)} - {traceback.format_exc()}')

    try:
        Stromzaehler.send_data()
        Variables.get_logger().log('Successfully send data to Messstellenbetreiber.')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        Variables.get_logger().log(f'Sending data to Messstellenbetreiber failed! Fehler: {exc_type}: {str(e)} - {traceback.format_exc()}')
