import unittest
import consumer
import pika

class TestConsumerFunction(unittest.TestCase):
    def test_consume_from_queue(self):
        # Test valid RabbitMQ credentials
        consumer.consume_from_queue("candidatemq.n2g-dev.net", "cand_62cm", "3ITMjTgArIDmesgX", "cand_62cm", "cand_62cm_results")

        # Test invalid RabbitMQ credentials
        with self.assertRaises(pika.exceptions.AMQPConnectionError):
            consumer.consume_from_queue("candidatemq.n2g-dev.net", "invalid_username", "invalid_password", "cand_62cm", "cand_62cm_results")

if __name__ == "__main__":
    unittest.main()
