from api import API
from rabbitmq import RabbitMQ
from consumer import Consumer
from database import Database
import json

# Opening JSON file
f = open('config.json')
  
# Returns JSON object as a dictionary
config = json.load(f)

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

    # Consuming
    try:
        # Start consuming messages
        consumer.start_consuming()
    except KeyboardInterrupt:
        # Stop consuming messages
        consumer.stop_consuming()

if __name__ == "__main__":
    main()