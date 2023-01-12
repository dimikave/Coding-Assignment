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
    # Initialize the API client
    api = API(api_hostname)

    # Initialize RabbitMQ client
    rabbitmq = RabbitMQ(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)

    # Initialize the consumer
    consumer = Consumer(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)
    
    # Initialize the Database client
    db = Database(database_hostname, database_username, database_password,database_name)

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

            # Store the results
            db.store_results(data=filtered_results, reinit=False, flag=published_flag)

            # Read results in the database (optional)
            # print("Results TABLE:",db.read_results())


    # Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
    except KeyboardInterrupt:
        # Close the connection
        rabbitmq.connection.close()
    
if __name__ == "__main__":
    main()