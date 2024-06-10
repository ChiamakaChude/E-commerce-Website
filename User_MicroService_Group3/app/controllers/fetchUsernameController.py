from flask import Blueprint, jsonify, request, json, session
from models.fetchUsername import get_username

fetch_username_bp = Blueprint("getUsername",__name__)

#This function is for the product microservice. It makes a call to this
#endpoint to fetch a user's username when they want to add a product review
@fetch_username_bp.route("/user/getUsername", methods=["POST"])
def username():

    user_id = session.get("user_id") #gets session data

    #if user_id: #if user is logged in

    if request.method == 'POST':

        #User data from front end
        data = request.get_json()
        userID = data.get("id")

            

        username= get_username(userID) #Send user info to database

        return jsonify({"username" : username}), 200
    
    else:
        return {"error" : "null"}
    #else:
     #   return {"error" : "User not logged in"}