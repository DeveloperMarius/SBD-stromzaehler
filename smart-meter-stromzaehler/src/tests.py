import unittest
from variables import Variables
from app import Stromzaehler
from utils import get_current_milliseconds
import time
import requests
from dotenv import load_dotenv
import os


class AppTest(unittest.TestCase):

    def setUp(self):
        Variables.get_database().clear_database()

    @classmethod
    def setUpClass(self):
        load_dotenv()

    def test_simulate_energyusage(self):
        # Running function to test
        Stromzaehler.simulate_energyusage()
        current_timestamp = get_current_milliseconds()

        # Get results from database
        Variables.get_database().cursor.execute('SELECT * FROM readings')
        results_1 = Variables.get_database().cursor.fetchall()

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
        Variables.get_database().cursor.execute('SELECT * FROM readings')
        current_timestamp_2 = get_current_milliseconds()

        # Get results from database
        Variables.get_database().cursor.execute('SELECT * FROM readings ORDER BY timestamp DESC')
        results_2 = Variables.get_database().cursor.fetchall()

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

        # Collecting logs
        Variables.get_database().cursor.execute('SELECT * FROM logs')
        result_logs = Variables.get_database().cursor.fetchall()
        self.assertEqual(len(result_logs), 2)

    def test_server_reachable(self):
        response = None
        try:
            response = requests.get(f'{os.getenv("URL")}{"/healthcheck"}')
        except Exception as e:
            pass
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
