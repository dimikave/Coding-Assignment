import unittest
import requests_mock
import api

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = api.API('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results')

    @requests_mock.Mocker()
    def test_get_results(self, mock):
        # Set up the mock response
        mock.get('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results', json={'test': 'data'}, status_code=200)

        # Call the method being tested
        results = self.api.get_results()

        # Verify that the request was made and the response is as expected
        self.assertTrue(mock.called)
        self.assertEqual(results, {'test': 'data'})

    @requests_mock.Mocker()
    def test_get_results_failure(self, mock):
        # Set up the mock response
        mock.get('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results', status_code=404)

        # Call the method being tested
        results = self.api.get_results()

        # Verify that the request was made and the response is as expected
        self.assertTrue(mock.called)
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
