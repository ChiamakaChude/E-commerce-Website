from flask import Blueprint, jsonify, request, json, session, redirect
from config import KAFKA_SERVER

from models.getUsers import fetch_user_info

from kafka import KafkaConsumer

consumer = KafkaConsumer("review_events", bootstrap_servers=KAFKA_SERVER)

def getusers(user_id):

    pass


for message in consumer:

    event_data = json.loads(message.value.decode())
    user_id = event_data["user_id"]
    username = getusers(user_id)