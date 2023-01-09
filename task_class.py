import json
import pika
import requests
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

# Load configuration from a file
with open('config.json') as f:
    config = json.load(f)

# API endpoint and message queue details
api_endpoint = config['api_endpoint']
mq_host = config['mq_host']
mq_username = config['mq_username']
mq_password = config['mq_password']
mq_exchange = config['mq_exchange']
mq_queue = config['mq_queue']

# Database details
db_host = config['db_host']
db_username = config['db_username']
db_password = config['db_password']
db_name = config['db_name']

class MessageQueue:
    def __init__(self, host, username, password, exchange, queue):
        self.host = host
        self.username = username
        self.password = password
        self.exchange = exchange
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))
        self.channel = self.connection.channel()
    
    def close(self):
        self.connection.close()
    
    def declare_exchange(self):
        try:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct", passive=True)
        except pika.exceptions.ChannelClosedByBroker:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct")
            

    def declare_queue(self):
        try:
            self.channel.queue_declare(queue=self.queue, passive=True)
        except pika.exceptions.ChannelClosedByBroker:
            self.channel.queue_declare(queue=self.queue)

        # Retrieve the queue's statistics
            queue_stats = self.channel.queue_declare(queue=self.queue, passive=True)

            # Check the number of messages in the queue
            if queue_stats.method.message_count > 0:
                print("\n\n\n\n There are messages in the queue.")
            else:
                print("There are no messages in the queue.")    
    
    def bind_queue(self):
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue)

    def send_message(self, routing_key, message):
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=json.dumps(message))

    def start_consumer(self, callback):
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

class Database:
    def __init__(self, host, username, password, name):
        self.host = host
        self.username = username
        self.password = password
        self.name = name
    
    def connect(self):
        self.conn = mysql.connector.connect(user=self.username, password=self.password, host=self.host, database=self.name)
    
    def close(self):
        self.conn.close()
    
    def insert_message(self, message):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO results (gateway_eui, profile, endpoint, cluster, attribute, timestamp, value) VALUES (%s, %s, %s, %s, %s, %s, %s)", (message["gateway_eui"], message["profile"], message["endpoint"], message["cluster"], message["attribute"], message["timestamp"], message["value"]))
        self.conn.commit()
        cursor.close()

def handle_message(channel, method_frame, header_frame, body):
    message = json.loads(body)
    logging.info(f"Received message: {message}")

    # Store the message in the database
    db = Database(db_host, db_username, db_password, db_name)
    db.connect()
    db.insert_message(message)
    db.close()


def consume_api():
    # Consume data from the API
    response = requests.get(api_endpoint)
    if response.status_code != 200:
        logging.error(f"Failed to consume API. Status code: {response.status_code}")
        return
    results = response.json()
    logging.info(results)
    # print(results)

    # Send each piece of data to the exchange
    # Convert the gateway EUI from hexadecimal to decimal
    gateway_eui = int(results["gatewayEui"], 16)
    profile = int(results["profileId"],16)
    endpoint = int(results["endpointId"],16)
    cluster = int(results["clusterId"],16)
    attribute = int(results["attributeId"],16)
    timestamp = results["timestamp"]
    value = results["value"]

    # Construct the routing key in the required format
    routing_key = f"{gateway_eui}.{profile}.{endpoint}.{cluster}.{attribute}"

    message = {
        "timestamp": timestamp,
        "value": value,
    }
    mq = MessageQueue(mq_host, mq_username, mq_password, mq_exchange, mq_queue)
    mq.connect()
    mq.declare_exchange()
    mq.declare_queue()
    mq.bind_queue()
    mq.send_message(routing_key, message)
    mq.close()
    print(f"API endpoint: {api_endpoint}")
    print(f"API response: {response.text}")
    print(f"API results: {results}")

def main():
    mq = MessageQueue(mq_host, mq_username, mq_password, mq_exchange, mq_queue)
    mq.connect()
    mq.declare_exchange()
    mq.declare_queue()
    mq.bind_queue()
    mq.start_consumer(handle_message)

    # mq.start_consumer(handle_message)

    # Consume data from the API and send it to the exchange
    while True:
        consume_api()
        print('hey')


if __name__ == '__main__':
    main()