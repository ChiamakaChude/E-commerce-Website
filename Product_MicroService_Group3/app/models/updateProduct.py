import pyodbc
from flask import jsonify
from models.database_connection import connect_db



def update_product_info(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        
        #insert data into reviews and ratings table
        update_product_query = '''UPDATE dbo.ProductCatalog 
SET 
    Price = CASE WHEN ? IS NOT NULL THEN ? ELSE Price END,
    StockQuantity = CASE WHEN ? IS NOT NULL THEN ? ELSE StockQuantity END
WHERE 
    ProductID = ?;'''
        cursor.execute(update_product_query, (data["price"], data["price"], data["quantity"], data["quantity"], data["product_id"]))
        


        #Commit changes to database if no errors
        connection.commit()

        return {"message" : "Product updated successfully"}
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in add_review: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in add_review: {e}")
        connection.rollback() #Rollback if errors
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()