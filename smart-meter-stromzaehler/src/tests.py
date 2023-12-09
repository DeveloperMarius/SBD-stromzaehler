import unittest
from variables import Variables
from app import Stromzaehler
from utils import get_current_milliseconds
import time
import requests
from dotenv import load_dotenv
import signal
import subprocess
from time import sleep
import os
import json
import hashlib
from cryptography.hazmat.primitives import serialization
import jwt


class AppTest(unittest.TestCase):
    flask_server = None

    def get_test_db(self):
        return Variables.get_database(f"{os.path.dirname(os.path.realpath(__file__))}/../generated/database-1.db")

    def setUp(self):
        self.get_test_db().clear_database()

    @classmethod
    def setUpClass(self):
        load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../generated/.env-1")
        print("Starting Flask Server...")
        self.flask_server = subprocess.Popen(["python3", f"{os.path.dirname(os.path.realpath(__file__))}/../../smart-meter-messstellenbetreiber/src/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)
        print("Started")

    @classmethod
    def tearDownClass(self):
        print("\nClosing Flask Server...")
        os.killpg(os.getpgid(self.flask_server.pid), signal.SIGTERM)

    def test_simulate_energyusage(self):
        # Running function to test
        Stromzaehler.simulate_energyusage()
        current_timestamp = get_current_milliseconds()

        # Get results from database
        self.get_test_db().cursor.execute('SELECT * FROM readings')
        results_1 = self.get_test_db().cursor.fetchall()

        # Checking number of results
        self.assertEqual(len(results_1), 1)

        # Checking zaehlerstand value
        value = results_1[0]['value']
        self.assertLessEqual(value, 28)
        self.assertLessEqual(18, value)

        # Checking timestamp
        timestamp = results_1[0]['timestamp']
        self.assertLessEqual(current_timestamp - 1000, timestamp)
        self.assertLessEqual(timestamp, current_timestamp + 1000)

        # Waiting one second to avoid same timestamp for first and second database entry
        time.sleep(1)

        # Checking second call of function
        Stromzaehler.simulate_energyusage()
        self.get_test_db().cursor.execute('SELECT * FROM readings')
        current_timestamp_2 = get_current_milliseconds()

        # Get results from database
        self.get_test_db().cursor.execute('SELECT * FROM readings ORDER BY timestamp DESC')
        results_2 = self.get_test_db().cursor.fetchall()

        # Checking number of results
        self.assertEqual(len(results_2), 2)

        self.assertEqual(results_1[0]['id'], results_2[1]['id'])

        # Checking zaehlerstand value
        value_2 = results_2[0]['value']
        self.assertLessEqual(value_2, 2 * 28)
        self.assertLessEqual(2 * 18, value_2)

        # Checking timestamp
        timestamp_2 = results_2[0]['timestamp']
        self.assertLessEqual(current_timestamp_2 - 1000, timestamp_2)
        self.assertLessEqual(timestamp_2, current_timestamp_2 + 1000)

    def test_send_data(self):
        strom = Stromzaehler()
        strom.simulate_energyusage()
        strom.simulate_energyusage()

        # Collecting readings
        self.get_test_db().cursor.execute('SELECT * FROM readings')
        result_readings = self.get_test_db().cursor.fetchall()
        self.assertEqual(len(result_readings), 2)

        # Collecting Logs
        self.get_test_db().cursor.execute('SELECT * FROM logs')
        result_logs = self.get_test_db().cursor.fetchall()
        self.assertEqual(len(result_logs), 0)

        # Send data
        body = json.dumps({
            'readings': result_readings,
            'logs': result_logs
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
        response = requests.post('http://localhost:5000/api/stromzaehler/update', headers={'Authorization': jwt_token, 'Content-Type': 'application/json'}, data=body)

        # Check response code
        self.assertEqual(response.status_code, 200)

        token = response.headers["Authorization"].split(" ")[-1]

        key = serialization.load_pem_public_key((os.getenv('MESSSTELLENBETREIBER_PUBLIC_KEY').replace('\\n', '\n').encode()))
        jwt_body = jwt.decode(token, key, algorithms=['EdDSA'], options={"verify_signature": False})

        self.assertIn('mode', jwt_body)
        self.assertEqual(jwt_body['mode'], 'SHA256')
        self.assertIsNotNone(jwt_body['signature'], jwt_body)
        actual_hash = hashlib.sha256(json.dumps(response.json()).encode('utf-8')).hexdigest()
        self.assertEqual(actual_hash, jwt_body['signature'])

    def test_server_reachable(self):
        response = None
        try:
            response = requests.get('http://localhost:5000/api/healthcheck')
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
