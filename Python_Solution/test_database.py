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
        """
        Set up test data and create a new instance of the Database class
        """

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

    # Testing how to store results
    def test_store_results(self):
        """
        Test storing data in the database

        Verifies:
            - The data is stored correctly in the database
        """

        # Test storing data in the database
        self.db.store_results(self.data)

        # Check if the data is stored correctly
        results = self.db.read_results()
        self.assertEqual(results[-1][0], self.data["gatewayEui"])
        self.assertEqual(results[-1][1], self.data["profileId"])
        self.assertEqual(results[-1][2], self.data["endpointId"])
        self.assertEqual(results[-1][3], self.data["clusterId"])
        self.assertEqual(results[-1][4], self.data["attributeId"])
        self.assertEqual(results[-1][5], self.data["timestamp"])
        self.assertEqual(results[-1][6], self.data["value"])


    def test_reinit_database(self):
        """
        Test that the reinit_database method correctly clears the database
        
        Verifies:
            - The results table is empty after calling the reinit_database method
        """

        # Create a new instance of the Database class
        db = Database(self.hostname, self.username, self.password, self.database)
        
        # Store first to check later if the data are deleted indeed
        db.store_results(self.data)
        
        # Call the reinit_database method
        db.reinit_database()
        
        # Check that the results table is empty
        results = db.read_results()
        self.assertEqual(len(results), 0)

    def test_read_results(self):
        """
        Test that the read_results method correctly retrieves data from the database

        Verifies:
            - The returned results contain the test data
        """
        
        # Create a database object
        db = Database(self.hostname, self.username, self.password, self.database)
        
        # Insert test data into the database
        db.store_results(self.data)
        
        # Call the read_results method
        results = db.read_results()
        
        # Assert that the returned results contain the test data
        self.assertIn(tuple(self.data.values()), results)

if __name__ == '__main__':
    unittest.main()