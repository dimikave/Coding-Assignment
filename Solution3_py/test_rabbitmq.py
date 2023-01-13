
import unittest
from rabbitmq import RabbitMQ
import json
import pika

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

class TestRabbitMQ(unittest.TestCase):

    def test_send_to_exchange(self):
        """
        Test that the send_to_exchange method correctly sends messages to the exchange
        
        Verifies:
            - The filtered_results and published_flag match expected values
        """

        # Set up test inputs
        hostname = rabbitmq_hostname
        username = rabbitmq_username
        password = rabbitmq_password 
        exchange = rabbitmq_exchange
        queue = rabbitmq_queue
        results = {
            "gatewayEui": hex(9574384526953556788),
            "profileId": hex(260),
            "endpointId": hex(10),
            "clusterId": hex(1794),
            "attributeId": hex(1024),
            "timestamp": 1673519598131,
            "value": 2341
        }

        # Initialize RabbitMQ object and call the send_to_exchange method
        self.rabbitmq = RabbitMQ(hostname, username, password, exchange, queue)
        filtered_results, published_flag = self.rabbitmq.send_to_exchange(results)

        # Assert that the filtered_results and published_flag match expected values
        self.assertEqual(filtered_results, {
            "gatewayEui": 9574384526953556788,
            "profileId": 260,
            "endpointId": 10,
            "clusterId": 1794,
            "attributeId": 1024,
            "timestamp": 1673519598131,
            "value": 2341
        })
        self.assertTrue(published_flag)

    def test_send_to_exchange_failure(self):
        """
        Test that the send_to_exchange method fails when an invalid exchange is passed
        
        Verifies:
            - The exception is of type ChannelWrongStateError
            - The published_flag remains False
        """
        
        # Set up test inputs
        hostname = rabbitmq_hostname
        username = rabbitmq_username
        password = rabbitmq_password 
        exchange = "not_existing_exchange"
        queue = rabbitmq_queue
        results = {
            "gatewayEui": hex(int("9574384526953556788")),
            "profileId": hex(int("260")),
            "endpointId": hex(int("10")),
            "clusterId": hex(int("1794")),
            "attributeId": hex(int("1024")),
            "timestamp": 1673519598131,
            "value": 2341
        }

        # Try to initialize RabbitMQ, but because of the wrong credentials it fails and
        # raises the ChannelWrongStateError because the channel is closed. Thus, the published
        # flag remains False, thus the test fail
        published_flag=False
        try:
            self.rabbitmq = RabbitMQ(hostname, username, password, exchange, queue)
            filtered_results, published_flag = self.rabbitmq.send_to_exchange(results)
        except Exception as e:
            self.assertIsInstance(e, pika.exceptions.ChannelWrongStateError)
            
        self.assertFalse(published_flag)

if __name__ == '__main__':
    unittest.main()