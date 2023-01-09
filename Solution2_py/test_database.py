import unittest
import database
import mysql.connector

class TestDatabaseFunctions(unittest.TestCase):
    def test_store_in_database(self):
        # Test valid database credentials
        data = {
            "gatewayEui": 1234567890,
            "profileId": 1,
            "endpointId": 2,
            "clusterId": 3,
            "attributeId": 4,
            "timestamp": 5,
            "value": 6.0
        }
        database.store_in_database(data, False, "candidaterds.n2g-dev.net", "cand_62cm", "3ITMjTgArIDmesgX", "cand_62cm")

        # Test invalid database credentials
        with self.assertRaises(mysql.connector.errors.ProgrammingError):
            data = {
                "gatewayEui": 1234567890,
                "profileId": 1,
                "endpointId": 2,
                "clusterId": 3,
                "attributeId": 4,
                "timestamp": 5,
                "value": 6.0
            }
            database.store_in_database(data, False, "candidaterds.n2g-dev.net", "invalid_username", "invalid_password", "cand_62cm")
    
    def test_read_from_database(self):
        # Test valid database credentials
        records = database.read_from_database("candidaterds.n2g-dev.net", "cand_62cm", "3ITMjTgArIDmesgX", "cand_62cm")
        self.assertIsInstance(records, list)
        
        # Test invalid database credentials
        with self.assertRaises(mysql.connector.errors.ProgrammingError):
            records = database.read_from_database("candidaterds.n2g-dev.net", "invalid_username", "invalid_password", "cand_62cm")

if __name__ == "__main__":
    unittest.main()