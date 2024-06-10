from flask import Blueprint, jsonify, request, session
from kafka import KafkaConsumer
import json
from config import KAFKA_SERVER

show_reviews_bp = Blueprint("showReviews", __name__)


consumer_conf = {
    "bootstrap_servers": KAFKA_SERVER,
    "group_id": "show_reviews_group", 
    "auto_offset_reset": "earliest"   
}

#Function to consume reviews published by product microservice
def consume_reviews(num_reviews=1):
    consumer = KafkaConsumer("customer_reviews", **consumer_conf)
    reviews = []
    

    for message in consumer:

        review_data_str = message.value.decode("utf-8")
        

        review_data = json.loads(review_data_str)
        

        reviews.append(review_data)
        

        if len(reviews) >= num_reviews:
            break


    consumer.close()

    return reviews


#Route to show reviews for a user
@show_reviews_bp.route("/user/showReviews", methods=["POST"])
def show_reviews():
    #Collect user id from session
    user_id = session.get("user_id")

    if user_id:  # Check if user is logged in
        if request.method == 'POST':
            #Call function to consume reviews
            reviews = consume_reviews()

            return jsonify(reviews)
        else:
            return {"message": "null"}
    else:
        return {"error": "User not logged in"}
