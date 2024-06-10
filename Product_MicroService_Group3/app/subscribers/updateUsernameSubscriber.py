from kafka import KafkaConsumer

from config import KAFKA_SERVER

from models.updateUsername import update_username

from threading import Thread


import json
import logging

#This function is called in the "__init__.py" file in the "subscribers" folder
def consume_username_updated_event():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Consuming username updated event...")
    consumer = KafkaConsumer("profile_updated_topic", bootstrap_servers=KAFKA_SERVER)
    for message in consumer: #Consume data
        profile_data_str = message.value.decode("utf-8")
        profile_data = json.loads(profile_data_str)
        print("I am here")
        print(profile_data)
        update_username(profile_data)

def start_kafka_consumer():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Kafka consumer...")
    print("Hello from kafka consumer")
    kafka_thread = Thread(target=consume_username_updated_event)
    kafka_thread.daemon = True  #Threading to avoid blocking of the Flask server logs
    kafka_thread.start()        