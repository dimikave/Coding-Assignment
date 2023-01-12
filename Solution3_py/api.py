import requests
import json

class API:
    def __init__(self, hostname):
        self.hostname = hostname
    
    def get_results(self):
        """Make a GET request to the API and return the results"""
        response = requests.get(self.hostname)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to retrieve data from API")
            return []
