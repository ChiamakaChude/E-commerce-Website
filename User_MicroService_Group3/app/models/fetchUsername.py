from flask import jsonify
import pyodbc
from models.database_connection import connect_db


def get_username(id):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT Username FROM dbo.User_table where UserID = ?"
        cursor.execute(query, id)

        row = cursor.fetchone() #fetch data

        if row:
            return row[0] 
        else:
            return None

        #connection.close()

        return username
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in fetch_user_info: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in get_username: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
