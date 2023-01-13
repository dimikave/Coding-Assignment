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

# Credentials for Database
database_hostname = config["database"]["hostname"]
database_username = config["database"]["username"]
database_password = config["database"]["password"]
database_name = config["database"]["database"]


def main():
    """
    The main() starts by loading configurations from the config.json
    file, which includes the hostname, username, password and other settings 
    for the API, RabbitMQ and Database. Then, it initializes the API, Publisher
    (RabbitMQ) and Consumer.
    
    A try-except & a while loop are used to continuously consume data from the 
    API and publish it to the queue. It also uses a counter to reattempt publishing 
    a message that failed to be published. 
    
    If a KeyboardInterrupt (Ctrl+C) is caught, the connection of the publisher to the 
    queue is closed and we then proceed to consuming.
    Through a try-except we start consuming messages. If a KeyboardInterrupt (Ctrl+C) 
    is caught, the connection of the consumer to the queue is closed and the consumer
    stops consuming messages.
    Finally, the content of the database after message consumption from the queue is printed.
    """

    # Initialize the API client
    api = API(api_hostname)

    # Initialize RabbitMQ client
    rabbitmq = RabbitMQ(rabbitmq_hostname,
                rabbitmq_username,
                rabbitmq_password,
                rabbitmq_exchange, 
                rabbitmq_queue)

    # Initialize the consumer
    consumer = Consumer(rabbitmq_hostname, 
                rabbitmq_username, 
                rabbitmq_password, 
                rabbitmq_exchange, 
                rabbitmq_queue, 
                database_hostname, 
                database_username, 
                database_password, 
                database_name)

    # If we want to, we can empty the database first, comment the following line if not:
    consumer.db.reinit_database()

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
    
    # Consuming
    try:
        # Start consuming messages and store the results through callback of consumer
        consumer.start_consuming()
    except KeyboardInterrupt:
        # Stop consuming messages
        consumer.stop_consuming()
    
    print("\n Database after message consumption from queue: \n", consumer.db.read_results())


if __name__ == "__main__":
    main()