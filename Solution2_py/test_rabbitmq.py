import unittest
import rabbitmq
import pika

class TestRabbitMQFunctions(unittest.TestCase):
    def test_send_to_exchange(self):
        # Test valid RabbitMQ credentials and valid results
        results = {
            "gatewayEui": "9574384526953556788",
            "profileId": "260",
            "endpointId": "10",
            "clusterId": "1794",
            "attributeId": "1024",
            "timestamp": 1623481925,
            "value": 25.3
        }
        filtered_results = rabbitmq.send_to_exchange(results, "candidatemq.n2g-dev.net", "cand_62cm", "3ITMjTgArIDmesgX", "cand_62cm","cand_62cm_results")
        self.assertIsInstance(filtered_results, dict)
        
        # Test invalid RabbitMQ credentials
        with self.assertRaises(pika.exceptions.AMQPConnectionError):
            filtered_results = rabbitmq.send_to_exchange(results, "candidatemq.n2g-dev.net", "invalid_username", "invalid_password", "cand_62cm","cand_62cm_results")
        
        # Test invalid results
        with self.assertRaises(KeyError):
            filtered_results = rabbitmq.send_to_exchange({}, "candidatemq.n2g-dev.net", "cand_62cm", "3ITMjTgArIDmesgX", "cand_62cm", "cand_62cm_results")

if __name__ == "__main__":
    unittest.main()
