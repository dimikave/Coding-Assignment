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

def main():
    # Initialize the consumer
    consumer = Consumer(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)
 
    # Consuming
    try:
        # Start consuming messages
        consumer.start_consuming()
    except KeyboardInterrupt:
        # Stop consuming messages
        consumer.stop_consuming()

if __name__ == "__main__":
    main()