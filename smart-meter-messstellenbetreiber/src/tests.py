import subprocess
import unittest
import requests
from dotenv import load_dotenv, dotenv_values
import os
from time import sleep
import hashlib
from cryptography.hazmat.primitives import serialization
import jwt
from models import Stromzaehler, Log
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils import Variables, get_current_milliseconds
import json
from datetime import datetime
import pytz


class AppTest(unittest.TestCase):
    flask_server = None

    @classmethod
    def setUpClass(cls):
        load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")
        print("Starting Flask Server...")
        cls.flask_server = subprocess.Popen(["python3", f"{os.path.dirname(os.path.realpath(__file__))}/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)
        print("Started")

    @classmethod
    def tearDownClass(cls):
        print("\nClosing Flask Server...")
        cls.flask_server.terminate()
        cls.flask_server.wait()
        print("Flask Server closed.")

    def setUp(self):
        Variables.get_database().clear_database()

    @staticmethod
    def generate_stromzaehler_jwt(body):
        jwt_data = {
            'type': 'stromzaehler',
            'id': 1,
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }
        values = dotenv_values(f"{os.path.dirname(os.path.realpath(__file__))}/../../smart-meter-stromzaehler/generated/.env-1")
        key = values['PRIVATE_KEY'].replace('\\n', '\n')
        private_key = serialization.load_pem_private_key(key.encode(), password=None)

        return 'Bearer ' + jwt.encode(jwt_data, private_key, "EdDSA", headers={'crv': 'Ed25519'})

    @staticmethod
    def generate_kundenportal_jwt(body, key_source='kundenportal'):
        jwt_data = {
            'type': 'kundenportal',
            'id': 1,
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }
        if key_source == 'kundenportal':
            values = dotenv_values(f"{os.path.dirname(os.path.realpath(__file__))}/../../smart-meter-kundenportal/.env")
            key = values['SECRET_PRIVATE_KEY'].replace('\\n', '\n')
        elif key_source == 'messstellenbetreiber':
            key = os.getenv('PRIVATE_KEY').replace('\\n', '\n')
        else:
            return None
        private_key = serialization.load_pem_private_key(key.encode(), password=None)

        return 'Bearer ' + jwt.encode(jwt_data, private_key, "EdDSA", headers={'crv': 'Ed25519'})

    def test_healthcheck(self):
        response = None
        try:
            response = requests.get("http://localhost:5000/api/healthcheck")
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_body_checksum(self):
        body = {
            'a': 'b'
        }
        body2 = {
            'a': 'b2'
        }
        response = None
        try:
            response = requests.post('http://localhost:5000/api/stromzaehler/register', json=body, headers={
                'Authorization': self.generate_kundenportal_jwt(json.dumps(body2))
            })
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)

    def test_body_jwt_broken(self):
        body = {
            'a': 'b'
        }
        body_json = json.dumps(body)
        response = None
        try:
            response = requests.post('http://localhost:5000/api/stromzaehler/register', data=body_json, headers={
                'Authorization': f"{self.generate_kundenportal_jwt(body_json)}a",
                'Content-Type': 'application/json'
            })
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)

    def test_body_jwt_wrong_key(self):
        body = {
            'a': 'b'
        }
        body_json = json.dumps(body)
        response = None
        try:
            response = requests.post('http://localhost:5000/api/stromzaehler/register', data=body_json, headers={
                'Authorization': f"{self.generate_kundenportal_jwt(body_json, 'messstellenbetreiber')}",
                'Content-Type': 'application/json'
            })
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)

    def test_body_jwt_unset(self):
        body = {
            'a': 'b'
        }
        body_json = json.dumps(body)
        response = None
        try:
            response = requests.post('http://localhost:5000/api/stromzaehler/register', data=body_json, headers={
                'Content-Type': 'application/json'
            })
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)

    def test_register_stromzaehler(self):
        body = {
            'id': 1,
            'person': {
                'firstname': f"Max{get_current_milliseconds()}",
                'lastname': 'Musterfrau',
                'gender': 1,
                'phone': None,
                'email': None
            },
            'address': {
                'street': f"Musterstraße {get_current_milliseconds()}",
                'plz': 60385,
                'city': 'Frankfurt am Main',
                'state': 'Hessen',
                'country': 'Deutschland'
            }
        }
        body_json = json.dumps(body)
        response = None
        try:
            response = requests.post('http://localhost:5000/api/stromzaehler/register', data=body_json, headers={
                'Authorization': self.generate_kundenportal_jwt(body_json),
                'Content-Type': 'application/json'
            })
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        with Session(Variables.get_database().get_engin()) as session:
            statement = select(Stromzaehler).where(Stromzaehler.id == 1)
            response = session.scalar(statement)
            self.assertEqual(response.owner_obj.firstname, body['person']['firstname'])
            self.assertEqual(response.address_obj.street, body['address']['street'])

    def test_stromzaehler_update_and_history(self):
        # Testing stromzaehler_update
        local_tz = pytz.timezone('Europe/Berlin')

        stromzaehler_id = 1
        timestamp_1 = 1701385200000
        timestamp_2 = 1701471600000
        timestamp_3 = 1701471600000

        readings = [
            {
                "id": 1,
                "value": 10,
                "timestamp": timestamp_1
            },
            {
                "id": 2,
                "value": 11,
                "timestamp": timestamp_2
            },
            {
                "id": 3,
                "value": 11,
                "timestamp": timestamp_3
            }
        ]

        update_body = json.dumps({
            "readings": readings,
            "logs": []
        })
        update_response = requests.post('http://localhost:5000/api/stromzaehler/update',
                                        headers={"Authorization": AppTest.generate_stromzaehler_jwt(update_body),
                                                 'Content-Type': 'application/json'},
                                        data=update_body)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json(), {"success": True})

        # Testing stromzaehler history
        history1_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": local_tz.localize(datetime.fromtimestamp(timestamp_1 / 1000.0)).date().strftime('%Y-%m-%d'),
            "end_date": local_tz.localize(datetime.fromtimestamp(timestamp_2 / 1000.0)).date().strftime('%Y-%m-%d')
        })
        history1_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": AppTest.generate_kundenportal_jwt(history1_body),
                                                  'Content-Type': 'application/json'},
                                         data=history1_body)

        self.assertEqual(history1_response.status_code, 200)
        readings2 = sorted(history1_response.json()['readings'], key=lambda x: x['id'])
        self.assertEqual(readings2, readings)

        history2_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": local_tz.localize(datetime.fromtimestamp((timestamp_1 / 1000.0) - 60*60*24*2)).date().strftime('%Y-%m-%d'),
            "end_date": local_tz.localize(datetime.fromtimestamp((timestamp_1 / 1000.0) - (60*60*24*2))).date().strftime('%Y-%m-%d')
        })
        history2_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": AppTest.generate_kundenportal_jwt(history2_body),
                                                  'Content-Type': 'application/json'},
                                         data=history2_body)

        self.assertEqual(history2_response.status_code, 200)
        self.assertEqual(history2_response.json(), {"readings": []})

        history3_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": local_tz.localize(datetime.fromtimestamp((timestamp_2 / 1000.0) + (60*60*24*2))).date().strftime('%Y-%m-%d'),
            "end_date": local_tz.localize(datetime.fromtimestamp((timestamp_2 / 1000.0) + (60*60*24*2))).date().strftime('%Y-%m-%d')
        })
        history3_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": AppTest.generate_kundenportal_jwt(history3_body),
                                                  'Content-Type': 'application/json'},
                                         data=history3_body)

        self.assertEqual(history3_response.status_code, 200)
        self.assertEqual(history3_response.json(), {"readings": []})

    def test_input_validation(self):
        with Session(Variables.get_database().get_engin()) as session:
            try:
                entry = Log(
                    timestamp=1701385200000,
                    endpoint='/api',
                    method='GETTTTTTTTTTTTTTTTTTTTTTTTT',
                    source_type='stromzaehler',
                    source_id=1,
                    message=''
                )
                session.add(entry)
                session.commit()
                self.assertTrue(False)
            except Exception as e:
                self.assertTrue(True)
                session.rollback()

            try:
                entry = Log(
                    timestamp=1701385200000,
                    endpoint='/api',
                    method='GET',
                    source_type='stromzaehler',
                    source_id=1,
                    message=''
                )
                session.add(entry)
                session.commit()
                self.assertTrue(True)
            except Exception as e:
                print(e)
                self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
