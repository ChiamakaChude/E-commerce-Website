#This section allows a user to delete their profile
#

from flask import Blueprint, jsonify, request, session
from models.deleteProfile import delete

deleteProfile_bp = Blueprint("deleteProfile",__name__)

@deleteProfile_bp.route("/user/deleteProfile", methods=["POST"])
def deleteProfile():

    #collects user id from session
    user_id = session.get("user_id")

    if user_id:#checks if user is logged in

        if request.method == 'POST':

            #User data from front end
            data = request.get_json()
            email = data.get("email")

            user_info = {
                "email" : email,
                "user_id" : user_id
            }

            user = delete(user_info) #sends user data to database
            

            return jsonify(user, user_id)
        
        else:
            return {"message" : "null"}
    
    else:
        return {"error" : "User not logged in"}