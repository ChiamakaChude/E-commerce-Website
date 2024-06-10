from flask import Flask, jsonify, redirect, json, url_for, request, render_template, make_response, session, abort
from flask_cors import CORS
from flask import jsonify
from controllers.loginController import login_bp
from controllers.signupController import signup_bp
from controllers.updateProfileController import update_profile_bp
from controllers.changePasswordController import change_password_bp
from controllers.deleteProfileController import deleteProfile_bp
from controllers.logoutController import logout_bp
from controllers.fetchUsernameController import fetch_username_bp
from controllers.showReviewsController import show_reviews_bp

from config import DEBUG, SECRET_KEY, PORT, HOST
import os
import requests
import publishers



app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/hello/<int:score>")
def hello_user(score):
    return render_template("hello.html", marks=score)


app.register_blueprint(login_bp)

app.register_blueprint(signup_bp)

app.register_blueprint(update_profile_bp)

app.register_blueprint(change_password_bp)

app.register_blueprint(deleteProfile_bp)

app.register_blueprint(logout_bp)

app.register_blueprint(fetch_username_bp)

app.register_blueprint(show_reviews_bp)

publishers.create_profile_updated_topic()


#Check if application is running in docker to collect or set secret key
try:

    #Check for the existence of the /proc/self/cgroup file
    with open("/proc/self/cgroup", "r") as cgroup_file:
        cgroup_info = cgroup_file.read()

    #Check if the cgroup information contains 'docker' keyword
    if 'docker' in cgroup_info:
        print("Running inside Docker container")
        app.secret_key = os.environ.get('SECRET_KEY')
    
except FileNotFoundError:
    # If the file doesn't exist
    print("Running on a local Windows machine")

    app.secret_key = SECRET_KEY


@app.route("/userIDs", methods=["POST"])
def userIDs():

    #ids = request.json
    #print(ids)
    return 'hi'

if __name__ == '__main__':
    app.run(host=HOST, debug=DEBUG, port=PORT)