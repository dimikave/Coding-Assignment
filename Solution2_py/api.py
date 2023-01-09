import requests
import json

def get_results(api_hostname):
    # Make a GET request to the API
    response = requests.get(api_hostname)

    # Check the status code of the response to make sure the request was successful
    if response.status_code == 200:
        # Extract the data from the response
        data = response.json()
        return data
    else:
        print("Failed to retrieve data from API")
        return []
