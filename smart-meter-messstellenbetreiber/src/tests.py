import subprocess
import unittest
import requests
from dotenv import load_dotenv
import os
from time import sleep
import signal


class AppTest(unittest.TestCase):
    flask_server = None

    @classmethod
    def setUpClass(self):
        load_dotenv(f"{os.path.dirname(os.path.realpath(__file__))}/../res/.env")
        self.flask_server = subprocess.Popen(["python3", f"{os.path.dirname(os.path.realpath(__file__))}/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sleep(5)

    @classmethod
    def tearDownClass(self):
        os.killpg(os.getpgid(self.flask_server.pid), signal.SIGTERM)

    def test_healthcheck(self):
        response = requests.get("http://localhost:5000/api/healthcheck")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
