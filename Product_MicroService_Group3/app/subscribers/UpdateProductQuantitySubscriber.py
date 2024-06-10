from kafka import KafkaConsumer

from config import KAFKA_SERVER

from models.updateProductQuantity import update_product_quantity

from threading import Thread


import json
import logging

#This function is called in the "__init__.py" file in the "subscribers" folder
def consume_product_price_updated_event():
    #Logging information
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Consuming product price updated event...")
    consumer = KafkaConsumer("QuantityUpdateFromOrders", bootstrap_servers=KAFKA_SERVER)
    for message in consumer:
        product_data_str = message.value.decode("utf-8")
        product_data = json.loads(product_data_str)
        print("I am here")
        print(product_data)
        update_product_quantity(product_data)

def start_price_updated_consumer():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Kafka price updated consumer...")
    print("Hello from kafka consumer")
    kafka_thread = Thread(target=consume_product_price_updated_event)
    kafka_thread.daemon = True  #Threading to avoid blocking of the Flask server logs
    kafka_thread.start()        