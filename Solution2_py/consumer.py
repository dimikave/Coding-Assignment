import pika


def consume_from_queue(rabbitmq_hostname, rabbitmq_username, rabbitmq_password, rabbitmq_exchange, rabbitmq_queue):
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

    # Set up a callback function to process received messages
    def callback(ch, method, properties, body):
        # Process the message (e.g. store it in the database)
        print(f"------ Received message from queue: {body}")

    # # Start consuming messages from the queue
    try:
        # Consume messages from the queue
        channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)
        print("Waiting for messages. To exit, press Ctrl+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        # Stop consuming messages
        channel.stop_consuming()

        # Close the connection
        connection.close()






