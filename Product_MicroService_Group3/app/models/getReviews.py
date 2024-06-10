#from app import db
import pyodbc
from flask import jsonify
from models.database_connection import connect_db

#Function to get user info
def get_reviews(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        user_id = data

        #Get reviews from database
        reviews_query = "SELECT CustomerID, Username, Review, rating, ProductID FROM dbo.ReviewsAndRatings WHERE CustomerID= ?"
        cursor.execute(reviews_query, user_id)
        reviews = cursor.fetchall()

        reviews_data = [{"CustomerID": row[0], "Username": row[1], "Review": row[2], "rating" : row[3], "ProductID" : row[4]} for row in reviews]



        #connection.close()

        return (reviews_data)
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in get_review: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in get_review: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    