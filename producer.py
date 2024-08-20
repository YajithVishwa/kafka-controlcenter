from confluent_kafka import Producer

# Configuration for Kafka producer
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer',
}

# Create Producer instance
producer = Producer(**conf)

# Delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Producing a message
topic = 'test'

for i in range(10):
    message = f'Message {i}'
    producer.produce(topic, value=message, callback=delivery_report)
    producer.poll(0)  # Poll to trigger delivery report callbacks

# Flush any remaining messages in the buffer
producer.flush()

print("All messages sent successfully.")
