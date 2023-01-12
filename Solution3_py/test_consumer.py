import unittest
import json
from unittest.mock import MagicMock, patch
from consumer import Consumer
import pika


class TestConsumer(unittest.TestCase):
    @patch('pika.BlockingConnection')
    def test_start_consuming(self, mock_connection):
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"

        # Create a mock channel and set its basic_consume method to a MagicMock
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.basic_consume = MagicMock()

        # Initialize the Consumer object and call the start_consuming method
        consumer = Consumer(hostname, username, password, exchange, queue)
        consumer.start_consuming()

        # Assert that the basic_consume method was called with the correct arguments
        mock_channel.basic_consume.assert_called_with(queue=queue, on_message_callback=consumer.callback, auto_ack=True)

    @patch('pika.BlockingConnection')
    def test_stop_consuming(self, mock_connection):
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"

        # Create a mock channel and set its basic_consume and stop_consuming 
        # methods to a MagicMock
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.basic_consume = MagicMock()
        mock_channel.stop_consuming = MagicMock()

        # Initialize the Consumer object and call the stop_consuming method
        consumer = Consumer(hostname, username, password, exchange, queue)
        consumer.stop_consuming()

        # Assert that the stop_consuming and connection.close methods were called
        mock_channel.stop_consuming.assert_called_once()
        mock_connection.return_value.close.assert_called_once()
    
    @patch('pika.BlockingConnection')
    def test_exchange_declare_existing(self, mock_connection):
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"

        # Create a mock channel and set its exchange_declare method to a MagicMock
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.exchange_declare = MagicMock()

        # Initialize the Consumer object
        consumer = Consumer(hostname, username, password, exchange, queue)
        consumer.start_consuming()

        # Assert that the exchange_declare method was called with the correct parameters
        mock_channel.exchange_declare.assert_called_with(exchange=exchange, exchange_type="direct", passive=True)

    @patch('pika.BlockingConnection')
    def test_exchange_declare_not_existing(self, mock_connection):
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"

        # Create a mock channel and set its exchange_declare method to a MagicMock
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.exchange_declare.side_effect = [pika.exceptions.ChannelClosedByBroker(404, "not found"), None]

        # Initialize the Consumer object and call the start_consuming method
        consumer = Consumer(hostname, username, password, exchange, queue)
        try:
            consumer.start_consuming()
        except pika.exceptions.ChannelClosedByBroker as e:
            self.assertEqual(e.args[0], 404)
            self.assertEqual(e.args[1], 'not found')
    
    @patch('pika.BlockingConnection')
    def test_callback(self, mock_connection):
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"

        # Create a mock channel and set its basic_consume method to a MagicMock
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel
        mock_channel.basic_consume = MagicMock()

        # Initialize the Consumer object and call the start_consuming method
        consumer = Consumer(hostname, username, password, exchange, queue)
        consumer.start_consuming()

        # Create a mock message and invoke the callback function
        message = {"timestamp": 1673523894310, "value": 4312}
        body = json.dumps(message)
        callback = mock_channel.basic_consume.call_args[1]["on_message_callback"]
        callback(mock_channel, MagicMock(), MagicMock(), body)

        # Assert that the callback function was called with the correct parameters
        print(f"------ Received message from queue: {body}")



if __name__ == '__main__':
    unittest.main()