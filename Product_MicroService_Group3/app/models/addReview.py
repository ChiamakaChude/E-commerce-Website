import pyodbc
from flask import jsonify
from models.database_connection import connect_db



def add_user_review(data):

    try: #Error handling

        connection = connect_db()
        cursor = connection.cursor()

        
        #Insert data into reviews and ratings table
        insert_user_query = '''INSERT INTO dbo.ReviewsAndRatings (CustomerID, ProductID, Review, rating, Username)
VALUES (?, ?, ?, ?, ?);'''
        cursor.execute(insert_user_query, (data["UserID"], data["ProductID"], data["Review"], data["Rating"], data["Username"]))
        


        #Commit changes to database if no errors
        connection.commit()

        return {"message" : "Review added successfully"}
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in add_review: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in add_review: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()