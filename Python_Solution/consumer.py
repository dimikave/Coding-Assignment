import pika
from database import Database
import json
import functools

class Consumer:
    """
    A class that consumes messages from a specified RabbitMQ queue, processes them and stores them in a database.
    
    Attributes:
        hostname (str): The hostname of the RabbitMQ instance.
        username (str): The username used to connect to the RabbitMQ instance.
        password (str): The password used to connect to the RabbitMQ instance.
        exchange (str): The name of the exchange to consume messages from.
        queue (str): The name of the queue to consume messages from.
        db (Database): A Database object that is used to store results.
        channel (pika.adapters.blocking_connection.BlockingChannel): The channel used to consume messages from the queue.
    """
    def __init__(self, hostname, username, password, exchange, queue, db_hostname, db_username, db_password, db_database):
        """
        Consumer constructor.
        """
         
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
        """
        Start consuming messages from the specified queue,
        using the callback method defined in the class
        """

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
        """
        Stop consuming messages and close the connection
        """

        self.channel.stop_consuming()
        self.connection.close()
    
    # Set up a callback function to process received messages
    def callback(self,ch, method, properties, body):
        """
        A function to process received messages.
        
        Parameters:
            ch (pika.adapters.blocking_connection.BlockingChannel): The channel used to consume messages.
            method (pika.spec.Basic.Deliver): The method for the received messages. It includes routing_key which is used to extract information.
            properties (pika.spec.BasicProperties): The properties for the received messages.
            body (bytes): The message body.

        The function converts the message body from bytes to a Python dictionary, 
        and uses the routing key to extract information, by splitting it and zipping it with keys to make a data object.
        Then it updates the data with the body_json data.
        If the routing key is not empty, the data is stored in the database, otherwise it's printed that it was an empty message.
        """

        # Convert the message body from bytes to a Python dictionary
        message = json.loads(body)
        

        routing_key = method.routing_key
        routing_key_parts = routing_key.split(".")
        keys = ["gatewayEui", "profileId", "endpointId", "clusterId", "attributeId"]
        data = dict(zip(keys, routing_key_parts))

        body_json = json.loads(body)
        data.update(body_json)
        
    
        if (len(routing_key)>0):
        # Store the results
            self.db.store_results(data)
            print(f"------ Received message from queue: {body}")
            print("Results consumed and stored to database.")
        else:
            print("Results consumed, but it was an empty message.")
            print(f"------ Received message from queue: {body}")
