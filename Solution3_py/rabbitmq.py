import pika
import json
import time

MAX_RETRIES=2

class RabbitMQ:
    def __init__(self, hostname, username, password, exchange, queue):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.exchange = exchange
        self.queue = queue
        self.confirm_deliveries = False

        # Connect to the RabbitMQ instance
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            heartbeat=600,
            blocked_connection_timeout=300,
            host=self.hostname,
            credentials=pika.PlainCredentials(self.username, self.password)
        ))
        self.channel = self.connection.channel()
        self.channel.confirm_delivery()

        # Safely declare the queue and check if it is already declared
        try:
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct", passive=True, durable=True)
        except pika.exceptions.ChannelClosedByBroker:
            # Exchange does not exist, so we can proceed with declaring it
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="direct",durable=True)

    def send_to_exchange(self, results):
        gateway_eui = int(results["gatewayEui"], 16)
        profile = int(results["profileId"],16)
        endpoint = int(results["endpointId"],16)
        cluster = int(results["clusterId"],16)
        attribute = int(results["attributeId"],16)
        timestamp = results["timestamp"]
        value = results["value"]
        filtered_results = {
            "gatewayEui":gateway_eui, "profileId":profile,
            "endpointId": endpoint, "clusterId":cluster,
            "attributeId":attribute, "timestamp":timestamp, "value":value
        }
        # print("------ Filtered results in the queue:", filtered_results)


        # Build the routing key in the specified format
        routing_key = f"{gateway_eui}.{profile}.{endpoint}.{cluster}.{attribute}"

        message = {
            "timestamp": timestamp,
            "value": value,
        }
        print("Message sent:", message)

        # Initialize a retry counter and start attempting to publish the message
        retries = 0
        while retries < MAX_RETRIES:
            try:
                self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=routing_key,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(content_type='text/plain',
                                                    delivery_mode=pika.DeliveryMode.Persistent),
                    mandatory=True)
                print('Message was successfully published.')
                published_flag=True
                break
            except pika.exceptions.UnroutableError:
                retries += 1
                delay = 2 ** retries
                print(f'Message was returned, retrying in {delay} seconds.')
                time.sleep(delay)
                published_flag=False

        if (published_flag==False):
            print('Message was return as it reached maximum retries and failed to be published.')
                          
        self.channel.queue_bind(
            queue=self.queue,
            exchange=self.exchange,
            routing_key=routing_key
        )
        
        return filtered_results, published_flag

