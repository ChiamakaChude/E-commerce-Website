#from app import db
from flask import jsonify
import pyodbc
from models.database_connection import connect_db



def delete(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        email = data["email"]
        user_id = data["user_id"]

        # select user id from database
        id_check_query = "SELECT UserID from dbo.User_table WHERE UserID= ?"
        cursor.execute(id_check_query, user_id)
        user_row = cursor.fetchone()

        if user_row:
            userID = user_row[0] 
        else:
            return {"Error": "User not found"}
        
        #delete from authinfo table first because of foreign key constraint
        delete_authinfo_query = '''DELETE FROM dbo.AuthInfo WHERE UserID= ?'''
        cursor.execute(delete_authinfo_query, userID)


        #delete user info from user table 
        delete_user_query = '''DELETE FROM dbo.User_table WHERE UserID = ?'''
        cursor.execute(delete_user_query, userID)


    

        #commit changes to database if no errors
        connection.commit()

        return {"message" : "Account successfully deleted"}
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in delete: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in delete: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()