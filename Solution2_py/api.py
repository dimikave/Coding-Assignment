import requests

def get_results():
    # Make a GET request to the API
    response = requests.get("https://xqy1konaa2.execute-api.eu-west-1.amazonaws.com/prod/results")

    # Check the status code of the response to make sure the request was successful
    if response.status_code == 200:
        # Extract the data from the response
        data = response.json()
        return data
    else:
        print("Failed to retrieve data from API")
        return []
