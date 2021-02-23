from kafka import KafkaConsumer

consumer = KafkaConsumer('sample1', auto_offset_reset='earliest', group_id=None)
print('Starting Kafka Consumer')

# Recursively print all messages from Kafka Broker
for message in consumer:
    print(message)