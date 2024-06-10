#from app import db
from flask import jsonify
import pyodbc
from models.database_connection import connect_db


def fetch_user_info(id):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT First_name, Last_name FROM dbo.User_table where UserID = ?"
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