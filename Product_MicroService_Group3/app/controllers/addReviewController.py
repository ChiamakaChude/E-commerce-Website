from flask import Blueprint, jsonify, request, json, session
from models.addReview import add_user_review
from config import HOST, PORT

import requests


add_review_bp = Blueprint("addReview",__name__)

#This connects to the user microservice to get username when a user wants to add a review
#It uses a get method to get the product id
@add_review_bp.route("/product/<int:productID>/addReview", methods=["GET"])
def get_username_from_user_microservice(productID):

    user_id = session.get("user_id")

    if user_id: #Check if session is set
        if request.method == "GET":


            product_id = productID

            response = requests.post("http://127.0.0.1:5000/user/getUsername", json={"id": user_id}) #Send http request to user microservice
            if response.status_code == 200:
                username = response.json()["username"]
                userID = user_id
                session["username"] = username
                session["productID"] = product_id

                #Data in json format
                rating_info = {
                    "UserID" : userID,
                    "ProductID" : product_id,
                    "Username" : username
                }

                return rating_info
            else:
                return {"Error" : "Failed to retrieve username"}
            
            #return "You can review the product with ID: {}".format(product_id)
        
        else:
            return {"error" : "null"}
        
    else:
        return {"error" : "You need to be logged in to add a review"}
    


#Add a product review with the username gotten
@add_review_bp.route("/product/<int:productID>/addReview", methods=["POST"])
def add_review(productID):

    user_id = session.get("user_id")

    if user_id:
        if request.method == "POST":

            data = request.get_json()
            review = data.get("review")
            rating = data.get("rating")
            product_id = productID
            username = session.get('username')
            product_id = session.get('productID')

            if review.strip() != "": #Check if review is empty

                if username is None:
                    return {"error": "Username is not available"}

                # Check if product_id is available
                if product_id is None:
                    return {"error": "Product ID is not available"}

                #Check if rating is valid
                if isinstance(rating, int) and 1 <= rating <= 5:

                    review_info = {
                        "UserID" : user_id,
                        "ProductID" : product_id,
                        "Review" : review,
                        "Rating" : rating,
                        "Username" : username
                    }

                    user_review_message = add_user_review(review_info) #Send data to database
                    return user_review_message
                
                else:
                    return {"error" : "Rating must be an integer between 1 and 5"}
                
            else:
                return {"error" : "Review cannot be empty"}
            
        
        else:
            return {"error" : "null"}
        
    else:
        return {"error" : "You need to be logged in to add a review"}