import unittest
import requests_mock
import api

class TestAPI(unittest.TestCase):
    """
    A class for testing the API class. Inherits from unittest.TestCase.
    
    Attributes:
        api (api.API): An instance of the API class.
    """

    def setUp(self):
        """
        Initialize an instance of the API class for testing.
        """
        self.api = api.API('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results')

    @requests_mock.Mocker()
    def test_get_results(self, mock):
        """
        Test the get_results method of the API class.
        
        Args:
            mock (requests_mock.Mocker): A mock object to handle the request.
        
        Verifies:
            - The request is made and the response is as expected.
        """

        # Set up the mock response
        mock.get('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results', json={'test': 'data'}, status_code=200)

        # Call the method being tested
        results = self.api.get_results()

        # Verify that the request was made and the response is as expected
        self.assertTrue(mock.called)
        self.assertEqual(results, {'test': 'data'})

    @requests_mock.Mocker()
    def test_get_results_failure(self, mock):
        """
        Test the get_results method of the API class when an error occurs.
        
        Args:
            mock (requests_mock.Mocker): A mock object to handle the request.
        
        Verifies:
            - The request is made and the response is as expected.
        """
        
        # Set up the mock response
        mock.get('https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results', status_code=404)

        # Call the method being tested
        results = self.api.get_results()

        # Verify that the request was made and the response is as expected
        self.assertTrue(mock.called)
        self.assertEqual(results, {})

if __name__ == '__main__':
    unittest.main()
