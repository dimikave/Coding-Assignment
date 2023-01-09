import unittest
import api
import requests

class TestAPIFunction(unittest.TestCase):
    def test_get_results(self):
        # Test valid API hostname
        result = api.get_results("https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results")
        self.assertIsInstance(result, dict)
        
        # Test invalid API hostname
        with self.assertRaises(requests.exceptions.ConnectionError):
            result = api.get_results("https://invalid_hostname.execute-api.eu-west-1.amazonaws.com/prod/results")

if __name__ == "__main__":
    unittest.main()
