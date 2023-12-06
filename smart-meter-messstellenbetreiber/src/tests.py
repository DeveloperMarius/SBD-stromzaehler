import subprocess
import unittest
import requests
from dotenv import load_dotenv, dotenv_values
import os
from time import sleep
import signal
import json
import hashlib
from cryptography.hazmat.primitives import serialization
import jwt
from models import StromzaehlerLog, StromzaehlerReading, Stromzaehler, Person, Address
from sqlalchemy import select
from sqlalchemy.orm import Session
import sys
from utils import Variables, get_current_milliseconds


class AppTest(unittest.TestCase):
    flask_server = None

    @classmethod
    def setUpClass(self):
        load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")
        self.flask_server = subprocess.Popen(["python3", f"{os.path.dirname(os.path.realpath(__file__))}/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)

    @classmethod
    def tearDownClass(self):
        #save_stdout = sys.stdout
        #sys.stdout = open(r'/tmp/a')

        os.killpg(os.getpgid(self.flask_server.pid), signal.SIGTERM)

        # regain stdout to screen
        #sys.stdout.close()
        #sys.stdout = save_stdout


    def generate_kundenportal_jwt(self, body):
        jwt_data = {
            'type': 'kundenportal',
            'id': 1,
            'mode': "SHA256",
            'signature': hashlib.sha256(body.encode('utf-8')).hexdigest()
        }
        values = dotenv_values(f"{os.path.dirname(os.path.realpath(__file__))}/../../smart-meter-kundenportal/.env")
        key = values['SECRET_PRIVATE_KEY'].replace('\\n', '\n')
        private_key = serialization.load_pem_private_key(key.encode(), password=None)

        return 'Bearer ' + jwt.encode(jwt_data, private_key, "EdDSA", headers={'crv': 'Ed25519'})

    def test_healthcheck(self):
        response = requests.get("http://localhost:5000/api/healthcheck")
        self.assertEqual(response.status_code, 200)

    def test_register_stromzaehler(self):
        body = {
            'id': 1,
            'person': {
                'first_name': f"Max{get_current_milliseconds()}",
                'last_name': 'Musterfrau',
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
        response = requests.post('http://localhost:5000/api/stromzaehler/register', data=body_json, headers={
            'Authorization': self.generate_kundenportal_jwt(body_json),
            'Content-Type': 'application/json'
        })
        self.assertEqual(response.status_code, 200)
        with Session(Variables.get_database().get_engin()) as session:
            statement = select(Stromzaehler).where(Stromzaehler.id == 1)
            response = session.scalar(statement)
            #self.assertEqual(response.owner.first_name, body['person']['first_name'])
            #self.assertEqual(response.address.street, body['address']['street'])
            #print(response)


if __name__ == '__main__':
    unittest.main()
