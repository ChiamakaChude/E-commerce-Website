from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from config import KAFKA_SERVER

import json

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


#Creates the topic
def create_product_updated_topic():

    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_SERVER)

    #Set topic name
    topic_name = "product_updated_topic"
    num_partitions = 1
    replication_factor = 1

    #Get topics
    topic_metadata = admin_client.list_topics()

    #Check if the topic already exists
    if topic_name not in topic_metadata:

        new_topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

        admin_client.create_topics(new_topics=[new_topic], validate_only=False)


#Function is called in updateProfileControllers.py
def publish_product_updated_event(event_data):

    event_json = json.dumps(event_data)
    #Publish the event
    data_to_send = producer.send("product_updated_topic", value=event_json.encode("utf-8"))
    try:
        record_metadata = data_to_send.get(timeout=10)
        print("Message sent successfully!")
        print("Topic:", record_metadata.topic)
        print("Partition:", record_metadata.partition)
        print("Offset:", record_metadata.offset)
    except Exception as e:
        print("Failed to send message:", e)
    producer.flush()