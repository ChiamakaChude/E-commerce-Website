#from app import db
import pyodbc
from flask import jsonify
from models.database_connection import connect_db

#Function to get user info
def get_product_by_section(data):

    try: #error handling

        connection = connect_db()
        cursor = connection.cursor()

        category_id = data

        #Get image info from database
        product_section_query = """SELECT 
    t1.ProductID, 
    t1.ProductName, 
    t1.ProductDesc, 
    t1.Price, 
    t3.ProductCategoryID, 
    t3.CategoryName, 
    COALESCE(AVG(t4.Rating), 0) AS AverageRating,
    t5.ImageIdentifier
FROM 
    dbo.ProductCatalog AS t1 
INNER JOIN 
    dbo.ProductCategory AS t2 ON t1.ProductID = t2.ProductID  
INNER JOIN 
    dbo.Category AS t3 ON t2.ProductCategoryID = t3.ProductCategoryID
LEFT JOIN 
    dbo.ReviewsAndRatings AS t4 ON t1.ProductID = t4.ProductID
LEFT JOIN 
    dbo.ProductImage AS t5 ON t1.ProductID = t5.ProductID
WHERE 
    t3.ProductCategoryID = ?
GROUP BY 
    t1.ProductID, 
    t1.ProductName, 
    t1.ProductDesc, 
    t1.Price, 
    t3.ProductCategoryID, 
    t3.CategoryName,
    t5.ImageIdentifier;
"""
        
        cursor.execute(product_section_query, category_id)

        products = cursor.fetchall()#fetch data

        products_data = [{"ProductID": row[0], 
                          "ProductName": row[1], 
                          "ProductDesc": row[2], 
                          "Price" : row[3], 
                          "ProductCategoryID" : row[4], 
                          "CategoryName" : row[5], 
                          "AverageRating" : row[6], 
                          "ImageName" : row[7]} for row in products]



        #connection.close()

        return (products_data)
    
    except pyodbc.Error as e: #error handling
        print(f"Database error in get_product_by_section: {e}")
        return None
    
    except Exception as e: #error handling
        print(f"Unexpected error occured in get_product_by_section: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    