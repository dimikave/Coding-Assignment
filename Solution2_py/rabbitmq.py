import pika
import json

def send_to_exchange(results):
    # Connect to the RabbitMQ instance
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="candidatemq.n2g-dev.net",
        credentials=pika.PlainCredentials("cand_62cm", "3ITMjTgArIDmesgX")
    ))
    channel = connection.channel()

        # Check if the exchange already exists
    try:
        channel.exchange_declare(exchange="cand_62cm", exchange_type="direct", passive=True)
    except pika.exceptions.ChannelClosedByBroker:
        # Exchange does not exist, so we can proceed with declaring it
        channel.exchange_declare(exchange="cand_62cm", exchange_type="direct")

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
    print("Filtered results:",filtered_results)
    # Build the routing key in the specified format
    routing_key = f"{gateway_eui}.{profile}.{endpoint}.{cluster}.{attribute}"
    # print(routing_key)

    message = {
    "timestamp": timestamp,
    "value": value,
    }
    print("Message:" ,message)

    # Send the message to the exchange
    channel.basic_publish(
        exchange="cand_62cm",
        routing_key=routing_key,
        body=json.dumps(message),
        mandatory=True
    )

    # Set the queue for the filtered results
    channel.queue_bind(
        queue="cand_62cm_results",
        exchange="cand_62cm",
        routing_key=routing_key
    )
    return filtered_results
    