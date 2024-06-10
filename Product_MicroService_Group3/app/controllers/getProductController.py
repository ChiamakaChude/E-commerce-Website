from flask import Blueprint, jsonify, request, json, session
from models.getProduct import get_product


display_product_bp = Blueprint("product",__name__)

#Display product with a given product ID
@display_product_bp.route("/product/<int:productID>", methods=["GET"])
def display_product(productID):

    user_id = session.get("user_id")


    if request.method == 'GET':


        product_id = productID
            

        # Convert to JSON
        #json_user_data = json.dumps(user_data)

        product, images, reviews = get_product(product_id) #Retrieve product data from database
        customers = [review_data["CustomerID"] for review_data in reviews]


        return jsonify(customers,{"product" : product, "images" : images, "reviews" : reviews, "session" : user_id})
    
    else:
        return {"error" : "null"}