import requests
import json

class API:
    """
    A class that makes GET requests to a specified hostname.
    
    Attributes:
        hostname (str): The hostname to make the GET request to.
    """

    
    def __init__(self, hostname):
        """
        Initialize an API object.
        
        Parameters:
            hostname (str): The hostname to make the GET request to.
        """
        self.hostname = hostname

    
    def get_results(self):
        """
        Make a GET request to the API and return the results.
        
        Returns:
            data (dict): A dictionary of JSON data returned from the API,
            or an empty dict if the request was not successful.
        """
        response = requests.get(self.hostname)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to retrieve data from API")
            return {}