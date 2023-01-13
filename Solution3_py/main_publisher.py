from api import API
from rabbitmq import RabbitMQ
from consumer import Consumer
from database import Database
import json

# Opening JSON file
f = open('config.json')
  
# Returns JSON object as a dictionary
config = json.load(f)

# API url
api_hostname = config["api"]["hostname"]

# Credentials for RabbitMQ
rabbitmq_hostname = config["rabbitmq"]["hostname"]
rabbitmq_username = config["rabbitmq"]["username"]
rabbitmq_password = config["rabbitmq"]["password"]
rabbitmq_exchange = config["rabbitmq"]["exchange"]
rabbitmq_queue = config["rabbitmq"]["queue"]


def main():
    """
    The main_publisher starts by loading configurations from the config.json
    file, which includes the hostname, username, password and other settings 
    for the API and RabbitMQ. Then, it initializes the API and the Publisher (RabbitMQ).
    
    A try-except & a while loop are used to continuously consume data from the 
    API and publish it to the queue. It also uses a counter to reattempt publishing 
    a message that failed to be published. 
    
    If a KeyboardInterrupt (Ctrl+C) is caught, the connection of the publisher to the 
    queue is closed.

    Its purpose is to serve only as a publisher, so it can be used along with the
    main_consumer.py in different terminals (to publish and consume messages respectively).
    """
    # Initialize the API client
    api = API(api_hostname)

    # Initialize RabbitMQ client
    rabbitmq = RabbitMQ(rabbitmq_hostname,
                rabbitmq_username,
                rabbitmq_password,
                rabbitmq_exchange, 
                rabbitmq_queue)

    
    # Consuming data from the API, attempting to publish to the queue, store results
    try:
        while(True):
            
            # Get data from the API
            results = api.get_results()

            # Flag
            published_flag=False
            counter = 0
            print('\n----------- New message attempt -------------')
            # Send the data to RabbitMQ -- Use of while to ensure that the message is going to be published
            while(published_flag==False):
                if (counter>0):
                    print('\nOne last try to publish the message:')
                    filtered_results, published_flag = rabbitmq.send_to_exchange(results)
                else:
                    filtered_results, published_flag = rabbitmq.send_to_exchange(results)
                counter += 1
            print('---------------------------------------------')
   
    # Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
    except KeyboardInterrupt:
        # Close the connection
        rabbitmq.connection.close()
    
if __name__ == "__main__":
    main()