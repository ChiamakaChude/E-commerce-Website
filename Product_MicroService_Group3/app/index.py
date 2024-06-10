from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort
from flask_cors import CORS
from flask import jsonify


from config import DEBUG, SECRET_KEY, PORT, HOST
import os
import requests
import subscribers

from controllers.getProductController import display_product_bp
from controllers.addReviewController import add_review_bp
from controllers.productHomeController import product_home_bp
from controllers.getReviewsController import get_review_bp
from controllers.updateProductController import update_product_bp




app = Flask(__name__)
CORS(app)



#Check if applcation is running in docker to get or set app secret key
try:

    #Check for the existence of the /proc/self/cgroup file
    with open("/proc/self/cgroup", "r") as cgroup_file:
        cgroup_info = cgroup_file.read()

    #Check if the cgroup information contains 'docker' keyword
    if 'docker' in cgroup_info:
        print("Running inside Docker container")
        app.secret_key = os.environ.get('SECRET_KEY')
    
except FileNotFoundError:
    #If the file doesn't exist
    print("Running on a local Windows machine")

    app.secret_key = SECRET_KEY


#subscribers.consume_username_updated_event()

@app.route('/product', methods=['POST'])
def get_session_id():
    session_id = session.get('user_id')
    if session_id:
        return jsonify({'session_id': session_id})
    else:
        return jsonify({'message': 'Session ID not found'})



@app.route('/')
def index():
    return render_template("index.html")



app.register_blueprint(display_product_bp)
app.register_blueprint(add_review_bp)
app.register_blueprint(product_home_bp)
app.register_blueprint(get_review_bp)
app.register_blueprint(update_product_bp)




if __name__ == '__main__':

    subscribers.start_kafka_consumer()
    subscribers.start_price_updated_consumer()

    app.run(host=HOST, debug=DEBUG, port=PORT)