import pyodbc
from flask import jsonify
from models.database_connection import connect_db
import logging



def update_product_quantity(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()
        print("At the database...")
        
        #Collect image information from database
        #stock_query = "SELECT StockQuantity FROM dbo.ProductCatalog WHERE ProductID = ?"
        #cursor.execute(stock_query, data["ProductID"])
        #stock = cursor.fetchall()

        #insert data into reviews and ratings table
        update_product_query = '''UPDATE dbo.ProductCatalog SET StockQuantity = StockQuantity - ? WHERE ProductID= ?;'''
        cursor.execute(update_product_query, (data["QuantityPurchased"], data["ProductID"]))
        


        #commit changes to database if no errors
        connection.commit()

        return {"message" : "Quantity updated successfully"}
        #return {"message" : stock}
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in update_product_quantity: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in update_product_quantity: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()