#from app import db
from flask import jsonify
import pyodbc
from models.database_connection import connect_db


def fetch_user_info(id):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT * FROM dbo.User_table where UserID = ?"
        cursor.execute(query, id)

        row = cursor.fetchone() #fetch data

        columns = [column[0] for column in cursor.description]
        user_data = dict(zip(columns, row))

        #connection.close()

        return user_data
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in fetch_user_info: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in fetch_user_info: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



def update_user(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()
        
        user_id = data["user_id"]

        #insert data into user table
        update_user_query = '''UPDATE dbo.User_table
    SET
        Username= ?,
        First_Name= ?,
        Last_Name= ?,
        Location= ?,
        Gender= ?
    WHERE
        UserID= ?'''

        cursor.execute(update_user_query, (data["first_name"], data["first_name"], data["last_name"], data["location"], data["gender"], user_id))


        #commit changes to database if no errors
        connection.commit()

        return {"message" : "Profile updated successfully"}
        


    except pyodbc.Error as e: #more error handling
        print(f"Database error in update_user: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in update_user: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()