from flask import Blueprint, jsonify, request, json, session
from models.productHome import get_product_by_section


product_home_bp = Blueprint("home",__name__)

#Display products on home page
@product_home_bp.route("/product/home", methods=["POST"])
def product_section():

    user_id = session.get("user_id")


    if request.method == 'POST':

        data = request.get_json()
        category_id = data.get("category_id")
            

        # Convert to JSON
        #json_user_data = json.dumps(user_data)

        products = get_product_by_section(category_id) #Get products


        return jsonify({"products" : products, "session" : user_id})
    
    else:
        return {"error" : "null"}