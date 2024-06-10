from flask import Blueprint, jsonify, request, json, session
from models.updateProduct import update_product_info
from publishers.kafkaPublishers import publish_product_updated_event

import requests


update_product_bp = Blueprint("updateProduct",__name__)

#Update a product
@update_product_bp.route("/product/updateProduct", methods=["POST"])
def update_product():

    user_id = session.get("user_id")

    if user_id:
        if request.method == 'POST':

            data = request.get_json()
            price = data.get("price")
            quantity = data.get("quantity")
            product_id = data.get("product_id")
            #username = session.get('username')

            #Check if price is int or float
            if isinstance(data.get("price"), (int, float)):
                
                #Check if quantity is int
                if isinstance(data.get("quantity"), int):
                    info = {
                        "quantity" : quantity,
                        "price" : price,
                        "product_id" : product_id
                    }

                    update = update_product_info(info) #Send updated info to database
                    if "message" in update:
                        event_data = {"quantity" : quantity, "price" : price, "product_id" : product_id}
                        publish_product_updated_event(event_data)

                        return {"Update Status": update}
                    else:
                        return {"error" : "error"}
                else:

                    return {"error" : "Quantity should be int"}
            else:
                return{"error" : "Price should be a number"}
            
               
        
        else:
            return {"error" : "null"}
        
    else:
        return {"error" : "You need to be logged in to update a product"}