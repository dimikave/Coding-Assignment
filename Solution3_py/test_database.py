import unittest
from database import Database
import json


# Opening JSON file
f = open('config.json')
  
# Returns JSON object as a dictionary
config = json.load(f)

# Credentials for Database
database_hostname = config["database"]["hostname"]
database_username = config["database"]["username"]
database_password = config["database"]["password"]
database_name = config["database"]["database"]


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.hostname = database_hostname
        self.username = database_username
        self.password = database_password
        self.database = database_name
        self.data = {
            "gatewayEui": 1234567890,
            "profileId": 1,
            "endpointId": 2,
            "clusterId": 3,
            "attributeId": 4,
            "timestamp": 1500000000,
            "value": 42.0
        }

        # Create a new instance of the Database class
        self.db = Database(self.hostname, self.username, self.password, self.database)

    def test_store_results(self):
        # Test storing data in the database
        self.db.store_results(self.data, True)

        # Check if the data is stored correctly
        results = self.db.read_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], self.data["gatewayEui"])
        self.assertEqual(results[0][1], self.data["profileId"])
        self.assertEqual(results[0][2], self.data["endpointId"])
        self.assertEqual(results[0][3], self.data["clusterId"])
        self.assertEqual(results[0][4], self.data["attributeId"])
        self.assertEqual(results[0][5], self.data["timestamp"])
        self.assertEqual(results[0][6], self.data["value"])

if __name__ == '__main__':
    unittest.main()