#from app import db
import pyodbc
from flask import jsonify
from models.database_connection import connect_db

#Function to get user info
def get_product(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        product_id = data

        #Get image info from database
        product_query = "SELECT * FROM dbo.ProductCatalog WHERE ProductID = ?"
        cursor.execute(product_query, product_id)

        row = cursor.fetchone() #fetch data

        columns = [column[0] for column in cursor.description]
        product_data = dict(zip(columns, row))

        #Collect image information from database
        image_query = "SELECT * FROM dbo.ProductImage WHERE ProductID = ?"
        cursor.execute(image_query, product_id)
        images = cursor.fetchall()

        image_data = [{"ImageIdentifier": row[0], "ProductID": row[1]} for row in images]


        #Get reviews from database
        reviews_query = "SELECT CustomerID, Username, Review, rating FROM dbo.ReviewsAndRatings WHERE ProductID= ?"
        cursor.execute(reviews_query, product_id)
        reviews = cursor.fetchall()

        reviews_data = [{"CustomerID": row[0], "Username": row[1], "Review": row[2], "rating" : row[3]} for row in reviews]



        #connection.close()

        return (product_data, image_data, reviews_data)
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in get_product: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in get_product: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    