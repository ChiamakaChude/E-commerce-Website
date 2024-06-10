import pyodbc
import os

#Code to connect to the database
print("Outside db connection function")
#Connect to database
def connect_db():
    print("In CONNECT DB")
    try:

        server = '34.89.83.33'
        database = 'productsmanagement'
        username = 'sqlserver'
        password = 'WebTechGroup3'
        driver = 'ODBC Driver 17 for SQL Server'

        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=no;'
      
        return pyodbc.connect(connection_string)
        
    except Exception as e:
        # If the file doesn't exist
        print("Unexpected error occured {e}")

        return False
