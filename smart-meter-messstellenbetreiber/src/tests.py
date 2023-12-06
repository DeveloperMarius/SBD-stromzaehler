import subprocess
import unittest
import requests
from dotenv import load_dotenv
import os
from time import sleep
import signal
import json
from datetime import datetime


class AppTest(unittest.TestCase):
    flask_server = None

    @classmethod
    def setUpClass(self):
        load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")
        self.flask_server = subprocess.Popen(["python3", f"{os.path.dirname(os.path.realpath(__file__))}/app.py"],
                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)

    @classmethod
    def tearDownClass(self):
        os.killpg(os.getpgid(self.flask_server.pid), signal.SIGTERM)

    def test_healthcheck(self):
        response = requests.get("http://localhost:5000/api/healthcheck")
        self.assertEqual(response.status_code, 200)

    def test_stromzaehler_update_and_history(self):
        # Testing stromzaehler_update
        stromzaehler_id = 1
        timestamp_1 = 1701876222272
        timestamp_2 = 1701876242272
        timestamp_3 = 1701876242274

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
                                        headers={"Authorization": self.get_jwt(), 'Content-Type': 'application/json'},
                                        data=update_body)
        self.assertEquals(update_response.status_code, 200)
        self.assertEquals(update_response.json, {"success": True})

        # Testing stromzaehler history
        history1_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": datetime.fromtimestamp(timestamp_1 / 1000.0).date().strftime('%Y-%m-%d'),
            "end_date": datetime.fromtimestamp(timestamp_2 / 1000.0).date().strftime('%Y-%m-%d')
        })
        history1_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": self.get_jwt(), 'Content-Type': 'application/json'},
                                         data=history1_body)

        self.assertEquals(history1_response.status_code, 200)
        self.assertEquals(history1_response.json, readings)

        history2_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": datetime.fromtimestamp((timestamp_1 - 2) / 1000.0).date().strftime('%Y-%m-%d'),
            "end_date": datetime.fromtimestamp((timestamp_1 - 2) / 1000.0).date().strftime('%Y-%m-%d')
        })
        history2_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": self.get_jwt(), 'Content-Type': 'application/json'},
                                         data=history2_body)

        self.assertEquals(history2_response.status_code, 200)
        self.assertEquals(history2_response.json, {"readings": []})

        history3_body = json.dumps({
            "stromzaehler_id": stromzaehler_id,
            "start_date": datetime.fromtimestamp(timestamp_2 / 1000.0).date().strftime('%Y-%m-%d'),
            "end_date": datetime.fromtimestamp((timestamp_2 + 1) / 1000.0).date().strftime('%Y-%m-%d')
        })
        history3_response = requests.get('http://localhost:5000/api/stromzaehler/history',
                                         headers={"Authorization": self.get_jwt(), 'Content-Type': 'application/json'},
                                         data=history3_body)

        self.assertEquals(history3_response.status_code, 200)
        self.assertEquals(history3_response.json, {"readings": [readings[1]]})


if __name__ == '__main__':
    unittest.main()
