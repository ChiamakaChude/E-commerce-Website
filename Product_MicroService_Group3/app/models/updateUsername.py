#from app import db
from flask import jsonify
import pyodbc
from models.database_connection import connect_db


def update_username(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()
        
        user_id = data["user_id"]
        username = data["new_username"]

        #insert data into user table
        update_user_query = '''UPDATE dbo.ReviewsAndRatings
    SET
        Username= ?
    WHERE
        CustomerID= ?'''

        cursor.execute(update_user_query, (username, user_id))


        #commit changes to database if no errors
        connection.commit()

        return {"message" : "Username updated successfully"}
        


    except pyodbc.Error as e: #more error handling
        print(f"Database error in update_username: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in update_username: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()