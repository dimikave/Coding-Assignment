import pika
import json

# Opening JSON file
f = open('config.json')
  
# returns JSON object as 
# a dictionary
config = json.load(f)


def send_to_exchange(results, rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue):
    # Connect to the RabbitMQ instance
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_hostname,
        credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    ))
    channel = connection.channel()

        # Check if the exchange already exists
    try:
        channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type="direct", passive=True)
    except pika.exceptions.ChannelClosedByBroker:
        # Exchange does not exist, so we can proceed with declaring it
        channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type="direct")

    # Extract the values from the result
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
    print("------ Filtered results in the queue:",filtered_results)
    # Build the routing key in the specified format
    routing_key = f"{gateway_eui}.{profile}.{endpoint}.{cluster}.{attribute}"
    # print(routing_key)

    message = {
    "timestamp": timestamp,
    "value": value,
    }
    print("Message sent:" ,message)

    # Send the message to the exchange
    channel.basic_publish(
        exchange=rabbitmq_exchange,
        routing_key=routing_key,
        body=json.dumps(message),
        mandatory=True
    )
    

    # Set the queue for the filtered results
    channel.queue_bind(
        queue=rabbitmq_queue,
        exchange=rabbitmq_exchange,
        routing_key=routing_key
    )
    
    return filtered_results