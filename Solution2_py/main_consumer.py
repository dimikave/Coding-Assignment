# Import the necessary functions
from api import get_results
from rabbitmq import send_to_exchange
from consumer import consume_from_queue
from database import store_in_database, read_from_database
import pika 
import json
import time

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

# # Connect to the RabbitMQ instance
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     host=rabbitmq_hostname,
#     credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
# ))
# channel = connection.channel()

# 4. Consume from queue
consume_from_queue(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)

# channel.close()
# connection.close()

