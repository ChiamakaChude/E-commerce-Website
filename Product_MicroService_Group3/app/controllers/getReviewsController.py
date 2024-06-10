from flask import Blueprint, jsonify, request, json, session
from models.getReviews import get_reviews
from config import KAFKA_SERVER

from kafka import KafkaProducer

#This gets reviews posted by a certain user
get_review_bp = Blueprint("getReview",__name__)

@get_review_bp.route("/product/getReview", methods=["POST"])
def get_review():

    user_id = session.get("user_id")

    if user_id:
        if request.method == 'POST':    

            #data = request.get_json()
            #review = data.get("review")

            get_reviews_by_user = get_reviews(user_id)

            send_review_message(get_reviews_by_user)

            return({"reviews" : get_reviews_by_user})
        
        else:
            return {"error" : "null"}
        
    else:
        return {"error" : "You need to be logged in to add a review"}
    

producer = KafkaProducer(bootstrap_servers = KAFKA_SERVER)

def send_review_message(reviews):
    #Publish message
    metadata =producer.send("customer_reviews", json.dumps(reviews).encode("utf_8"))
    try:
        record_metadata = metadata.get(timeout=10)
        #Print out message for confirmation in logs
        print("Message sent successfully!")
        print("Topic:", record_metadata.topic)
        print("Partition:", record_metadata.partition)
        print("Offset:", record_metadata.offset)
    except Exception as e:
        print("Failed to send message:", e)