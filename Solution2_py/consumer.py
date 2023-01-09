import pika

def consume_from_queue():
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

    # Set up a callback function to process received messages
    def callback(ch, method, properties, body):
        # Process the message (e.g. store it in the database)
        print(f"Received message: {body}")

    # Start consuming messages from the queue
    channel.basic_consume(
        queue="cand_62cm_results",
        on_message_callback=callback,
        auto_ack=True
    )
    try:
        # Consume messages from the queue
        channel.basic_consume(queue="cand_62cm_results", on_message_callback=callback, auto_ack=True)
        print("Waiting for messages. To exit, press Ctrl+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        # Stop consuming messages
        channel.stop_consuming()

        # Close the connection
        connection.close()






