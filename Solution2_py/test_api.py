import unittest
import api

class TestAPIFunction(unittest.TestCase):
    def test_get_results(self):
        # Test valid API hostname
        results = api.get_results("https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results")
        # self.assertTrue(isinstance(results, dict))
        # self.assertGreaterEqual(len(results), 0)

        # Test invalid API hostname
        results = api.get_results("https://invalid-api-hostname.com/prod/results")
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
