#This section allows a user to log in

from flask import Blueprint, jsonify, request, session
from models.login import fetch_user
from models.login import fetch_password
import hashlib
import secrets
import hmac

login_bp = Blueprint("login",__name__)

@login_bp.route("/login", methods=["POST"])
def login():

    if request.method == 'POST':

        #User data from front end
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        

        user = fetch_user(email) #Collect user data from database
        
        #User authentication
        if user is not None: #If database found matching email the user entered

            user_email = user.get("Email") #User email from database


            if user_email == email: #Checks if email returned from database is the same as what user entered
                
                auth = fetch_password(user_email) #function returns certain columns collected from database

                user_hash = auth.get("PasswordHash")
                user_salt = auth.get("PasswordSalt")
                user_iterations = auth.get("Iterations")


                #password authentication
                password_info = generate_password_hash(password)
                is_correct = verify_password(password_info, password, user_salt, user_iterations, user_hash)

                if is_correct == True: #if password is correct
                    session["user_id"] = user.get("UserID")
                    response_data = {"message":"Login Sucessful", "email": email, "session" : session["user_id"]}
                    return jsonify(response_data)
                
                else:
                    response_data = {"message":"Email or password incorrect", "email": email}
                    return jsonify(response_data)

                
            else:
                return ("Email does not exist")
            
        else:
            response_data = {"message":"Email does not exist", "email": email}
            return jsonify(response_data)
    
    return {"message" : "null"}
    

#password encryption
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

#password verification
def verify_password(stored_password_info, submitted_password, salt, iterations, user_hash):
    # Convert the stored salt back to bytes
    salt = bytes.fromhex(salt)
    # Use the same number of iterations as when the password was hashed
    iterations = iterations
    # Hash the submitted password with the stored salt and iterations
    hash = hashlib.pbkdf2_hmac('sha256', submitted_password.encode(), salt, iterations)
    
    # Compare the newly generated hash with the stored hash
    # Convert the generated hash to hex for comparison
    
    return hmac.compare_digest(hash.hex(), user_hash)