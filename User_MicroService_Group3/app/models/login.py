#from app import db
import pyodbc
from flask import jsonify
from models.database_connection import connect_db

#Function to get user info
def fetch_user(email):

    try: #error handling
        print("In FETCH USER")
        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT * FROM dbo.User_table where Email = ?"
        cursor.execute(query, email)

        row = cursor.fetchone() #fetch data

        columns = [column[0] for column in cursor.description]
        user_data = dict(zip(columns, row))

        #connection.close()

        return user_data
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in fetch_user: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in fetch_user: {e}")
        return None
    

    



#Fetch user's password
def fetch_password(email):

    try:

        connection = connect_db()
        cursor = connection.cursor()

        query = "SELECT t1.Email, t1.UserID, t2.Iterations, t2.PasswordHash, t2.PasswordSalt FROM dbo.User_table as t1 INNER JOIN dbo.AuthInfo as t2 ON t1.UserID = t2.UserID where Email= ?"
        
        cursor.execute(query, email)

        row = cursor.fetchone()

        if row is None:
            return {"message" : "Email does not exist"}

        else:
            columns = [column[0] for column in cursor.description]
            user_data = dict(zip(columns, row))

            #connection.close()

            return user_data
    
    except pyodbc.Error as e:
        print(f"Database error in fetch_user: {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected error occured in fetch_user: {e}")
        return None
    
 