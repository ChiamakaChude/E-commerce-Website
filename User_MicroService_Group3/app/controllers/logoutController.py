#This section allows a user to log out

from flask import Blueprint, jsonify, request, json, session, redirect


logout_bp = Blueprint("logout",__name__)

@logout_bp.route("/logout", methods=["POST"])
def logout():

    user_id = session.get("user_id") #get session data

    if user_id: #if user is logged in

        if request.method == 'POST':

            session.pop("user_id", None) #deletes session
            return ({"message" : "Log out successful"})
        
        else:
            return {"error" : "null"}
    else:
        return {"error" : "User not logged in"}