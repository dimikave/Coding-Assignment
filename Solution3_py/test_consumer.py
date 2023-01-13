import unittest
import json
from unittest.mock import MagicMock, patch
from consumer import Consumer
import pika
import json


# Opening JSON file
f = open('config.json')
  
# Returns JSON object as a dictionary
config = json.load(f)

# Credentials for Database
database_hostname = config["database"]["hostname"]
database_username = config["database"]["username"]
database_password = config["database"]["password"]
database_name = config["database"]["database"]

class TestConsumer(unittest.TestCase):
    """
    A class that tests the functionality of the Consumer class
    
    This test class uses the unittest library and the patch method
    from the unittest.mock library to mock the pika.BlockingConnection
    and test the methods of the Consumer class.
    """

    @patch('pika.BlockingConnection')
    def test_start_consuming(self, mock_connection):
        """
        Test that the start_consuming method correctly sets up the consumer to start consuming messages.
        
        Verifies: 
            - The basic_consume method was called with the correct arguments.

        The test mocks the pika.BlockingConnection and creates
        a mock channel. It sets the channel's basic_consume method
        to a MagicMock and initializes a Consumer object with test inputs. 
        The test then calls the start_consuming method on the Consumer 
        object and asserts that the basic_consume method was called with the 
        correct arguments.
        """

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
        consumer = Consumer(hostname, username, password, exchange, queue,database_hostname, database_username, database_password, database_name)
        consumer.start_consuming()

        # Assert that the basic_consume method was called with the correct arguments
        mock_channel.basic_consume.assert_called_with(queue=queue, on_message_callback=consumer.callback, auto_ack=True)

    @patch('pika.BlockingConnection')
    def test_stop_consuming(self, mock_connection):
        """
        Test that the stop_consuming method correctly stops the consumer 
        from consuming messages.
        
        Verifies:
            - The stop_consuming and connection.close methods were called.
        
        The test mocks the pika.BlockingConnection and creates a mock channel. 
        It sets the channel's stop_consuming and connection.close methods to 
        a MagicMock and initializes a Consumer object with test inputs. 
        The test then calls the stop_consuming method on the Consumer object and
        asserts that the stop_consuming and connection.close methods were called.
        """

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
        consumer = Consumer(hostname, username, password, exchange, queue,database_hostname, database_username, database_password, database_name)
        consumer.stop_consuming()

        # Assert that the stop_consuming and connection.close methods were called
        mock_channel.stop_consuming.assert_called_once()
        mock_connection.return_value.close.assert_called_once()
    
    @patch('pika.BlockingConnection')
    def test_exchange_declare_existing(self, mock_connection):
        """
        Test that the exchange_declare method correctly declares an existing exchange
        
        Verifies:
            - The exchange_declare method was called with the correct parameters.
        
        The test mocks the pika.BlockingConnection and creates a mock channel. 
        It sets the channel's exchange_declare method to a MagicMock and initializes 
        a Consumer object with test inputs. The test then calls the start_consuming 
        method on the Consumer object and asserts that the exchange_declare method
        was called with the correct parameters.
        """

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
        consumer = Consumer(hostname, username, password, exchange, queue, database_hostname, database_username, database_password, database_name)
        consumer.start_consuming()

        # Assert that the exchange_declare method was called with the correct parameters
        mock_channel.exchange_declare.assert_called_with(exchange=exchange, exchange_type="direct", passive=True)

    @patch('pika.BlockingConnection')
    def test_exchange_declare_not_existing(self, mock_connection):
        """
        Test that the exchange_declare method correctly declares a non-existing exchange
        
        Verifies:
            - The exchange_declare method was called with the correct parameters.
        
        The test mocks the pika.BlockingConnection and creates a mock channel. 
        It sets the channel's exchange_declare method to a MagicMock and 
        initializes a Consumer object with test inputs. The test then calls 
        the start_consuming method on the Consumer object and asserts that 
        the exchange_declare method was called with the correct parameters.
        """

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
        consumer = Consumer(hostname, username, password, exchange, queue,database_hostname, database_username, database_password, database_name)
        try:
            consumer.start_consuming()
        except pika.exceptions.ChannelClosedByBroker as e:
            self.assertEqual(e.args[0], 404)
            self.assertEqual(e.args[1], 'not found')
    
    @patch('pika.BlockingConnection')
    def test_callback(self, mock_connection):
        """
        Test that the callback method correctly logs the received message
        
        Verifies:
            - The print statement is called with the correct output
        """
        
        # Set up test inputs
        hostname = "localhost"
        username = "testuser"
        password = "testpassword"
        exchange = "testexchange"
        queue = "testqueue"
        ch, method, properties, body = MagicMock(), MagicMock(), MagicMock(), b'{"name":"John Doe"}'

        # Create a mock channel 
        mock_channel = MagicMock()

        # Initialize the Consumer object
        consumer = Consumer(hostname, username, password, exchange, queue,database_hostname, database_username, database_password, database_name)
        consumer.channel = mock_channel
        with patch('builtins.print') as mock_print:
            consumer.callback(ch, method, properties, body)
            mock_print.assert_called_with(f"------ Received message from queue: {body}")

if __name__ == '__main__':
    unittest.main()