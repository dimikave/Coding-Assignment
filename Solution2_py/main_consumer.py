# Import the necessary functions
from consumer import consume_from_queue
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


consume_from_queue(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)



