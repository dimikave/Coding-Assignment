# Import the necessary functions
from api import get_results
from rabbitmq import send_to_exchange
from consumer import consume_from_queue
from database import store_in_database, read_from_database
import pika 

# Retrieve the data from the API
results = get_results()

# Send the data to the RabbitMQ exchange
filtered_results = send_to_exchange(results)

# Connect to the RabbitMQ instance
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="candidatemq.n2g-dev.net",
    credentials=pika.PlainCredentials("cand_62cm", "3ITMjTgArIDmesgX")
))
channel = connection.channel()

# Check if there is a message in the queue
method_frame, header_frame, body = channel.basic_get(queue="cand_62cm_results")
if method_frame:
    print("There is a message in the queue.")
else:
    print("There are no messages in the queue.")

# Store the filtered results in the database
store_in_database(filtered_results)
print(read_from_database())

# Consume the filtered results from the queue
consume_from_queue()

# Check if there is a message in the queue
method_frame, header_frame, body = channel.basic_get(queue="cand_62cm_results")
if method_frame:
    print("There is a message in the queue.")
else:
    print("There are no messages in the queue.")


print(read_from_database)

