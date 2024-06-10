#This section allows a user to create a profile

from flask import Blueprint, jsonify, request, json
from models.signup import new_user
import hashlib
import secrets

signup_bp = Blueprint("signup",__name__)

@signup_bp.route("/signup", methods=["POST"])
def signup():

    if request.method == 'POST':

        #User data from front end
        data = request.get_json()
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        location = data.get("location")
        gender = data.get("gender")
        password = data.get("password")
        encoded_password = generate_password_hash(password)
        hash = encoded_password["hash"]
        salt = encoded_password["salt"]
        iterations = encoded_password["iterations"]

        if email.strip() != "": #checks if email is not empty (email cannot be null)
            
            # Create a dictionary from user data
            user_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "location": location,
                "gender": gender,
                "password": password,
                "hash": hash,
                "salt": salt,
                "iterations": iterations
            }

            # Convert to JSON
            json_user_data = json.dumps(user_data)


            update = new_user(user_data) #Send user info to database

            return jsonify(update)
        
        else:
            return {"error" : "email cannot be empty"}
    
    return {"error" : "null"}
    

#This function encrypts the user's password
def generate_password_hash(password):
    # Generate a 16-byte salt
    salt = secrets.token_bytes(16)
    # Define the number of iterations
    iterations = 100000
    # Generate the hash using PBKDF2-HMAC-SHA-256
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    
    # Return the salt, iterations, and hash, encoded in a way that can be stored in the database
    return {
        'salt': salt.hex(),
        'iterations': iterations,
        'hash': hash.hex()
    }
