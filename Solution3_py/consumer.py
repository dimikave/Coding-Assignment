import pika
from database import Database
import json
import functools

class Consumer:
    def __init__(self, hostname, username, password, exchange, queue, db_hostname, db_username, db_password, db_database):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.exchange = exchange
        self.queue = queue
        self.db = Database(db_hostname, db_username, db_password, db_database)
        self.channel = None

        # Connect to the RabbitMQ instance
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.hostname,
            credentials=pika.PlainCredentials(self.username, self.password)
        ))
        self.channel = self.connection.channel()

    def start_consuming(self):
        # Check if the exchange already exists
        try:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct", passive=True)
        except pika.exceptions.ChannelClosedByBroker:
            # Exchange does not exist, so we can proceed with declaring it
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct")

        # Start consuming messages from the queue
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print("Waiting for messages. To exit, press Ctrl+C")
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
        self.connection.close()
    
    # Set up a callback function to process received messages
    def callback(self,ch, method, properties, body):
        # Convert the message body from bytes to a Python dictionary
        message = json.loads(body)
        print(f"------ Received message from queue: {body}")

        routing_key = method.routing_key
        routing_key_parts = routing_key.split(".")
        keys = ["gatewayEui", "profileId", "endpointId", "clusterId", "attributeId"]
        data = dict(zip(keys, routing_key_parts))

        body_json = json.loads(body)
        data.update(body_json)
        
        if (len(routing_key)>0):
        # Store the results
            self.db.store_results(data)
            print("Results consumed and stored to database.")
        else:
            print("Results consumed, but it was an empty message.")
