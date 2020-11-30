import mysql.connector
from mysql.connector import Error
import datetime
from datetime import date
import pandas as pd
import random

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df1 = pd.read_csv('df_supplier.csv')
df1["supplier_id"] = df1.index + 1
df1.fillna(0, inplace=True)
df1 = df1.iloc[:, 1:]
print(df1.columns.values.tolist())
print(df1)

df2 = pd.read_csv('product_table.csv')
df2["product_id"] = df1.index + 1
df2.fillna(0, inplace=True)
df2 = df2.iloc[:, 1:]
print(df2.columns.values.tolist())
print(df2)

df5 = df1.merge(df2, left_on='supplier_id', right_on='product_id')
df5 = df5[['supplier_id','product_id']]
df5["SupplierToProduct_id"] = df5.index + 11111

print(df5)

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='aliexpress',
                                         user='root',
                                         password='110185')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        mySql_Create_Table_Query1 = """
        CREATE TABLE if not exists Supplier(
                                     nb_followers int(11) NOT NULL,
                                     name varchar(250) NOT NULL,
                                     store_no varchar(250) NOT NULL,
                                     country varchar(250) NOT NULL,
                                     opening_date date NOT NULL,
                                     supplier_id int(11) NOT NULL,
                                     PRIMARY KEY (supplier_id)) """

        mySql_Create_Table_Query2 = """
        CREATE TABLE if not exists Product(

                                     title varchar(250) NOT NULL,
                                     delivery varchar(250) NOT NULL,
                                     prices varchar(250) NOT NULL,
                                     qty_sold varchar(250) NOT NULL,
                                     ratings varchar(250) NOT NULL,
                                     stores varchar(250) NOT NULL,
                                     discounts varchar(250) NOT NULL,
                                     product_id int(11) NOT NULL, 
                                     PRIMARY KEY (product_id)) """

        mySql_Create_Table_Query5 = """
        CREATE TABLE if not exists SupplierToProduct (
                                     SupplierToProduct_id int(11) NOT NULL,
                                     supplier_id int(11) NOT NULL,                 
                                     product_id int(11) NOT NULL,                 
                 
                                     FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),                                     
                                     FOREIGN KEY (product_id) REFERENCES Product(product_id),
                                     PRIMARY KEY (SupplierToProduct_id))"""

        cursor = connection.cursor()
        result1 = cursor.execute(mySql_Create_Table_Query1)
        result2 = cursor.execute(mySql_Create_Table_Query2)
        result5 = cursor.execute(mySql_Create_Table_Query5)

        sql_str1 = "INSERT INTO Supplier (nb_followers, name, store_no, country, opening_date, supplier_id) VALUES (%s, %s, %s, %s, %s, %s)"

        sql_str2 = "INSERT INTO Product (title, delivery, prices, qty_sold, ratings, stores, discounts, product_id)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        sql_str5 = "INSERT INTO SupplierToProduct (SupplierToProduct_id, supplier_id, product_id) VALUES (%s, %s, %s)"

        cursor.executemany(sql_str1, df1.values.tolist())
        cursor.executemany(sql_str2, df2.values.tolist())
#        cursor.executemany(sql_str5, df5.values.tolist())

        connection.commit()

        print("Tables created successfully ")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")