#from app import db
from flask import jsonify
import pyodbc
from models.database_connection import connect_db


#Create a new user
def new_user(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        email = data["email"]

        # Check if the email already exists
        email_check_query = "SELECT COUNT(*) FROM dbo.User_table WHERE Email = ?"
        cursor.execute(email_check_query, email)
        count = cursor.fetchone()[0]

        if count > 0:
            return {"Error": "Email already exists"}

        
        #insert data into user table
        insert_user_query = '''INSERT INTO dbo.User_table (Username, Email, First_Name, Last_Name, Tenure_Months, Location, Gender)
VALUES (?, ?, ?, ?, ?, ?, ?);'''
        cursor.execute(insert_user_query, (data["first_name"], data["email"], data["first_name"], data["last_name"], " ", data["location"], data["gender"]))


        UserID_query = "SELECT UserID FROM dbo.User_table WHERE Email= ?"
        cursor.execute(UserID_query, email)
        UserID = cursor.fetchone()[0]


        #Insert password into authentication table
        insert_authinfo_query = '''INSERT INTO dbo.AuthInfo (PasswordHash, PasswordSalt, Iterations, TempPlainText, UserID)
VALUES (?, ?, ?, ?, ?);'''
        cursor.execute(insert_authinfo_query, (data["hash"], data["salt"], data["iterations"], data["password"], UserID))
        


        #commit changes to database if no errors
        connection.commit()

        return {"message" : "New user info added successfully"}
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in new_user: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in new_user: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()