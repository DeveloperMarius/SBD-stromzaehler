import subprocess
import unittest
import requests
from dotenv import load_dotenv, dotenv_values
import os
from time import sleep
import hashlib
from cryptography.hazmat.primitives import serialization
import jwt
from models import Stromzaehler, StromzaehlerReading, Alert
from sqlalchemy import select, delete
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
        cls.flask_server = subprocess.Popen(["python3",
                                             f"{os.path.dirname(os.path.realpath(__file__))}/app.py"])  # , stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)
        print("Started")

    @classmethod
    def tearDownClass(cls):
        print("\nClosing Flask Server...")
        cls.flask_server.terminate()
        cls.flask_server.wait()
        print("Flask Server closed.")

    @staticmethod
    def generate_stromzaehler_jwt(body):
        jwt_data = {
            'type': 'stromzaehler',
            'id': 1,
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }
        values = dotenv_values(
            f"{os.path.dirname(os.path.realpath(__file__))}/../../smart-meter-stromzaehler/generated/.env-1")
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

    @staticmethod
    def clear_stromzaehler_readings_and_alerts():
        with Session(Variables.get_database().get_engin()) as session:
            table = Alert.__table__
            delete_statement = delete(table)
            session.execute(delete_statement)
            table = StromzaehlerReading.__table__
            delete_statement = delete(table)
            session.execute(delete_statement)
            session.commit()

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
            response = requests.post('http://localhost:5000/api/stromzaehler/register', data=json.dumps(body), headers={
                'Authorization': self.generate_kundenportal_jwt(json.dumps(body2)),
                'Content-Type': 'application/json'
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
        self.clear_stromzaehler_readings_and_alerts()
        # Testing stromzaehler_update
        local_tz = pytz.timezone('Europe/Berlin')

        stromzaehler_id = 1
        timestamp_1 = 1701385200000
        timestamp_2 = 1701471600000
        timestamp_3 = 1701558000000

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
            "end_date": local_tz.localize(datetime.fromtimestamp(timestamp_3 / 1000.0)).date().strftime('%Y-%m-%d')
        })
        history1_response = requests.post('http://localhost:5000/api/stromzaehler/history',
                                          headers={"Authorization": AppTest.generate_kundenportal_jwt(history1_body),
                                                   'Content-Type': 'application/json'},
                                          data=history1_body)

        self.assertEqual(history1_response.status_code, 200)
        self.assertEqual(history1_response.json()['readings'], readings)

        history2_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": local_tz.localize(datetime.fromtimestamp((timestamp_1 - 2) / 1000.0)).date().strftime(
                '%Y-%m-%d'),
            "end_date": local_tz.localize(datetime.fromtimestamp((timestamp_1 - 2) / 1000.0)).date().strftime(
                '%Y-%m-%d')
        })
        history2_response = requests.post('http://localhost:5000/api/stromzaehler/history',
                                          headers={"Authorization": AppTest.generate_kundenportal_jwt(history2_body),
                                                   'Content-Type': 'application/json'},
                                          data=history2_body)

        self.assertEqual(history2_response.status_code, 200)
        self.assertEqual(history2_response.json(), {"readings": []})

        history3_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": local_tz.localize(datetime.fromtimestamp(timestamp_2 / 1000.0)).date().strftime('%Y-%m-%d'),
            "end_date": local_tz.localize(datetime.fromtimestamp((timestamp_2 + 1) / 1000.0)).date().strftime(
                '%Y-%m-%d')
        })
        history3_response = requests.post('http://localhost:5000/api/stromzaehler/history',
                                          headers={"Authorization": AppTest.generate_kundenportal_jwt(history3_body),
                                                   'Content-Type': 'application/json'},
                                          data=history3_body)

        self.assertEqual(history3_response.status_code, 200)
        self.assertEqual(history3_response.json()['readings'], [readings[1]])

    def test_alert_on_to_little_readings(self):
        # Deleting database entries in StromzaehlerReadings and Alerts
        self.clear_stromzaehler_readings_and_alerts()

        with Session(Variables.get_database().get_engin()) as session:
            # sending reading
            timestamp = 1702380120000
            readings = [
                {
                    "id": 1,
                    "timestamp": timestamp,
                    "value": 10
                },
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

            # Getting alerts
            statement = select(Alert)
            response = session.scalars(statement)
            alerts = response.fetchall()
            self.assertEqual(len(alerts), 0)

            # Testing insert correct reading
            readings = [
                {
                    "id": 2,
                    "timestamp": timestamp + Variables.get_cronjob_interval(),
                    "value": 11
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
            # Getting alerts
            statement = select(Alert)
            response = session.scalars(statement)
            alerts = response.fetchall()
            self.assertEqual(len(alerts), 0)

            # Testing insert false reading
            readings = [
                {
                    "id": 3,
                    "timestamp": timestamp + (3 * Variables.get_cronjob_interval()),
                    "value": 11
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
            # Getting alerts
            statement = select(Alert)
            response = session.scalars(statement)
            alerts = response.fetchall()
            self.assertEqual(len(alerts), 1)
            self.assertEqual(alerts[0].stromzaehler, 1)
            self.assertEqual(alerts[0].message, 'Stromzaehler collected to little readings!')

    def test_alert_on_lower_value(self):
        # Deleting database entries in StromzaehlerReadings and Alerts
        self.clear_stromzaehler_readings_and_alerts()

        with Session(Variables.get_database().get_engin()) as session:
            # sending reading
            timestamp = 1702380120000
            readings = [
                {
                    "id": 1,
                    "timestamp": timestamp,
                    "value": 10
                },
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
            # Getting alerts
            statement = select(Alert)
            response = session.scalars(statement)
            alerts = response.fetchall()
            self.assertEqual(len(alerts), 0)

            # sending reading
            timestamp = 1702380120000
            readings = [
                {
                    "id": 2,
                    "timestamp": timestamp + Variables.get_cronjob_interval(),
                    "value": 9
                },
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
            # Getting alerts
            statement = select(Alert)
            response = session.scalars(statement)
            alerts = response.fetchall()
            self.assertEqual(len(alerts), 1)
            self.assertEqual(alerts[0].stromzaehler, 1)
            self.assertEqual(alerts[0].message, 'Stromzaehler provided a smaller value than before!')

    def test_endpoint_alert(self):
        self.clear_stromzaehler_readings_and_alerts()

        timestamp = 1702380120000
        readings = [
            {
                "id": 1,
                "timestamp": timestamp,
                "value": 10
            },
            {
                "id": 2,
                "timestamp": timestamp + (2 * Variables.get_cronjob_interval()),
                "value": 11
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

        alert_body = json.dumps({
            "stromzaehler_id": 1
        })

        alert_response = requests.get('http://localhost:5000/api/stromzaehler/alerts',
                                      headers={"Authorization": AppTest.generate_kundenportal_jwt(alert_body),
                                               'Content-Type': 'application/json'},
                                      data=alert_body)
        self.assertEqual(alert_response.status_code, 200)
        with Session(Variables.get_database().get_engin()) as session:
            # Getting alert
            statement = select(Alert).where(Alert.id == 1)
            expected_alert = session.scalar(statement)
        data = alert_response.json()
        self.assertEqual(expected_alert.stromzaehler, data['alerts'][0]['stromzaehler_id'])
        self.assertEqual(expected_alert.id, data['alerts'][0]['id'])
        self.assertEqual(expected_alert.message, data['alerts'][0]['message'])
        self.assertEqual(expected_alert.timestamp, data['alerts'][0]['timestamp'])

    def test_kundenportal_endpoint_with_stromzaehler_credentials(self):
        body = json.dumps({
            "stromzaehler_id": 1
        })
        response = requests.get('http://localhost:5000/api/stromzaehler/alerts',
                                headers={"Authorization": AppTest.generate_stromzaehler_jwt(body),
                                         'Content-Type': 'application/json'},
                                data=body)
        self.assertEqual(response.status_code, 401)

    def test_stromzaehler_endpoint_with_kundenportal_credentials(self):
        timestamp = 1702380120000
        body = json.dumps({
            "readings": [
                {
                    "id": 1,
                    "timestamp": timestamp,
                    "value": 10
                },
                {
                    "id": 2,
                    "timestamp": timestamp + (2 * Variables.get_cronjob_interval()),
                    "value": 11
                }
            ],
            "logs": []
        })
        response = requests.post('http://localhost:5000/api/stromzaehler/update',
                                 headers={"Authorization": AppTest.generate_kundenportal_jwt(body),
                                          'Content-Type': 'application/json'},
                                 data=body)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
