from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuration settings for Kafka consumer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka server address
    'group.id': 'your_consumer_group_id',   # Specify your consumer group ID
    'auto.offset.reset': 'earliest',        # Start reading at the earliest message
}

# Create a Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the Kafka topic
topic = 'test'
consumer.subscribe([topic])

# Poll messages from Kafka
try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages with a timeout of 1 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                raise KafkaException(msg.error())

        # Print the received message
        print(msg)
        print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()} [{msg.partition()}]")

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
