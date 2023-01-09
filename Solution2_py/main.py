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

# Connect to the RabbitMQ instance
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_hostname,
    credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
))
channel = connection.channel()

# 1. Retrieve the data from the API
results = get_results(api_hostname)

# 2. Send the data to the RabbitMQ exchange
filtered_results = send_to_exchange(results, rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)

####### Following lines only exist for checking purposes
# Connect to the RabbitMQ instance
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_hostname,
    credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
))
channel = connection.channel()

# Check if there is a message in the queue
method_frame, header_frame, body = channel.basic_get(queue=rabbitmq_queue)
if method_frame:
    print("There is a message in the queue.")
else:
    print("There are no messages in the queue.")
#########

# 3. Store the filtered results in the database and print them
# Choose if you want to reinitialize the database
reinit = True 
store_in_database(filtered_results, reinit, database_hostname, database_username, database_password, database_name)
print("Database, results TABLE: ", read_from_database(database_hostname, database_username, database_password, database_name))

# 4. Consume the filtered results from the queue
time.sleep(1)
consume_from_queue(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue)

####### Following lines only exist for checking purposes
# Check if there is a message in the queue
method_frame, header_frame, body = channel.basic_get(queue=rabbitmq_queue)
if method_frame:
    print("There is a message in the queue.")
else:
    print("There are no messages in the queue.")

#########

channel.close()
connection.close()

