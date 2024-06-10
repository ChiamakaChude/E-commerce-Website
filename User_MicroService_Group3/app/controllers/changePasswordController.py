#This page allows users to change their password
#
#
from flask import Blueprint, jsonify, request, session
from models.changePassword import check_old_password, set_new_password
import hashlib
import secrets
import hmac

change_password_bp = Blueprint("change_password",__name__)

@change_password_bp.route("/user/change_password", methods=["POST"])
def change_password():

    user_id = session.get("user_id") #Get user ID from session

    if user_id:#checks if user is logges in

        if request.method == 'POST':

            #User data from front end
            data = request.get_json()
            email = data.get("email")
            old_password = data.get("old_password")
            new_password = data.get("new_password")

            new_encoded_password = generate_password_hash(new_password)
            new_password_hash = new_encoded_password["hash"]
            new_password_salt = new_encoded_password["salt"]
            new_password_iterations = new_encoded_password["iterations"]

            #collect old password, user id and email into json
            old_auth = {
                "user_id" : user_id,
                "email" : email,
                "password": old_password
            }

            #user_old_auth = check_old_password(old_auth) 
            

            #send old password to database            
            old_auth_info, value = check_old_password(old_auth) #function returns certain columns collected from database

            if value == 1: #if user exists in database

                old_password_hash = old_auth_info.get("PasswordHash")
                old_password_salt = old_auth_info.get("PasswordSalt")
                old_password_iterations = old_auth_info.get("Iterations")


                #password authentication. Calls password fucntions
                old_password_info = generate_password_hash(old_password)
                is_correct = verify_password(old_password_info, old_password, old_password_salt, old_password_iterations, old_password_hash)

                if is_correct == True:#if password is correct

                    #passes new password information to json
                    new_auth = {
                        "user_id" : user_id,
                        "email" : email,
                        "password": new_password,
                        "hash": new_password_hash,
                        "salt": new_password_salt,
                        "iterations": new_password_iterations
                    }

                    #sends new password to database
                    new_auth_info = set_new_password(new_auth)



                    response_data = {"message":"Password is correct"}
                    return jsonify(new_auth_info, user_id)
                
                else:
                    response_data = {"error":"Old password is incorrect", "email": email}
                    return jsonify(response_data)
                
            else:
                return {"error" : "Email does not exist"}
            
        
        return {"error" : "null"}
    
    else:
        return {"error" : "User not logged in"}

        

    

#password encoding
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