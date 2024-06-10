#This section allows a user to update their profile

from flask import Blueprint, jsonify, request, json, session
from models.updateProfile import update_user
from models.updateProfile import fetch_user_info

from events.eventDefinitions import updated_username
from publishers.kafkaPublishers import publish_username_updated_event

update_profile_bp = Blueprint("update",__name__)

@update_profile_bp.route("/user/update", methods=["POST"])
def update_profile():

    user_id = session.get("user_id") #gets session data

    if user_id: #if user is logged in

        user_info = fetch_user_info(user_id)
        print(jsonify(user_info))

        if request.method == 'POST':

            #User data from front end
            data = request.get_json()
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            location = data.get("location")
            gender = data.get("gender")

                
            # Create a json object from user data
            user_data = {
                "user_id" : user_id,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "location": location,
                "gender": gender,
            }

            update = update_user(user_data) #Send user info to database

            if "message" in update:

                event_data = {"user_id" : user_id, "new_username" : user_data["first_name"]}
                event_message = updated_username(user_id, user_data["first_name"])
                publish_username_updated_event(event_data)

                return jsonify({"Update Status": update, "Username" : user_data["first_name"], "User ID" : user_id, "Event message" : event_message})
        
        else:
            return {"error" : "null"}
    else:
        return {"error" : "User not logged in"}