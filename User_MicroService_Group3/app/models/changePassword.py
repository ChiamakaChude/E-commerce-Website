from flask import jsonify
import pyodbc
from models.database_connection import connect_db



def check_old_password(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        email = data["email"]
        user_id = data["user_id"]

        

        #Check if the email already exists
        email_check_query = "SELECT COUNT(*) FROM dbo.User_table WHERE UserID = ?"
        cursor.execute(email_check_query, user_id) #executes the query
        count = cursor.fetchone()[0]

        if count == 0:
            return ({"Error" : "Email does not exist"}, 0)
        
        else:
            #selects password information from database
            query = "SELECT t1.Email, t1.UserID, t2.Iterations, t2.PasswordHash, t2.PasswordSalt FROM dbo.User_table as t1 INNER JOIN dbo.AuthInfo as t2 ON t1.UserID = t2.UserID where t1.UserID= ?"
            
            cursor.execute(query, user_id) #executes query

            row = cursor.fetchone()

            columns = [column[0] for column in cursor.description]
            user_data = dict(zip(columns, row))

            #connection.close()

            return (user_data, 1)
    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in check_old_password: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in check_old_password: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def set_new_password(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        email = data["email"]
        user_id = data["user_id"]
        

        #selects user ID
        select_userID_query = "SELECT UserID from dbo.User_table where UserID = ?"
        cursor.execute(select_userID_query, user_id)
        UserID = cursor.fetchone()[0]


        #updates password
        update_authinfo_query = '''UPDATE dbo.AuthInfo
    SET PasswordHash = ?, PasswordSalt = ?, Iterations = ?, TempPlainText = ?
    WHERE UserID = ?'''
        

        cursor.execute(update_authinfo_query, (data["hash"], data["salt"], data["iterations"], data["password"], UserID))

        connection.commit()


        #connection.close()

        return {"Message" : "Password updated successfully"}
    

    
    except pyodbc.Error as e: #more error handling
        print(f"Database error in set_new_password: {e}")
        connection.rollback()
        return {"Error" : "Database error"}
    
    except Exception as e: #more error handling
        print(f"Unexpected error occured in set_new_password: {e}")
        connection.rollback()
        return {"Error" : "Unexpected error"}
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()