import mysql.connector
from mysql.connector import Error
import datetime
from datetime import date
import pandas as pd
import random

today = date.today()
date_1 = datetime.datetime.strptime(str(today), "%Y-%m-%d")

Supplier = list()
for i in range(1000,1003):
    dict_data1 = {
    'supplier_id': i,
    'nb_followers': i**2,
    'Name': 'name' + str(i),
    'store_no': 'store' + str(i),
    'country': 'country' + str(i),
    'opening_date': str(date_1 + datetime.timedelta(days=i)),
    }
    Supplier.append(dict_data1)
df1 = pd.DataFrame(Supplier)
print(df1)

Product = list()
for i in range(3000,3003):
    dict_data2 = {
    'product_id': i,
    'title': 'title' + str(i),
    'delivery': 'delivery' + str(i),
    'Price': random.random() * i,
    'quantity_sold': i,
    'rating': random.randint(1,5),
    'store': 'store' + str(i),
    'discount': random.randint(1,5),
    'available_quantity': i - 2000,
    }
    Product.append(dict_data2)
df2 = pd.DataFrame(Product)

print(df2)

Product_specifications = list()
for i in range(3000,3003):
    dict_data3 = {
    'product_id': i,
    'Brand_Name': 'Brand_Name' + str(i),
    'Video_Memory_Capacity': i**2,
    'Interface_Type': 'Interface_Type' + str(i),
    'Cooler_Type': 'Cooler_Type' + str(i),
    'Stream_Processors': i+i,
    'Chip_Process': 'Chip_Process' + str(i),
    'Model_Number': 'Model_Number' + str(i),
    'PixelPipelines': i,
    'Launch_Date': str(date_1 + datetime.timedelta(days=i)),
    'Output_Interface_Type1': 'Output_Interface_Type1' + str(i),
    'Output_Interface_Type2': 'Output_Interface_Type2' + str(i),
    'Memory_Interface': 'Memory_Interface' + str(i)
    }
    Product_specifications.append(dict_data3)
df3 = pd.DataFrame(Product_specifications)

print(df3)

Reviews = list()
for i in range(3000,3003):
    dict_data4 = {
    'review_id': i+1111,
    'product_id': i,
    'country': 'country' + str(i),
    'stars':  random.randint(1,5),
    'is_image': random.randint(0,1),
    'useful_yes': str(i * random.random()),
    'useful_no': str(i * random.random()),
    'date': str(date_1 + datetime.timedelta(days=i)),
    'text': str(i) + 'test'
    }
    Reviews.append(dict_data4)
df4 = pd.DataFrame(Reviews)

print(df4)

SupplierToProduct = list()
for i in range(3000,3003):
    dict_data5 = {
    'SupplierToProduct_id': int(i * random.random() + 9999),
    'supplier_id': i - 2000,
    'product_id':  i,
    }
    SupplierToProduct.append(dict_data5)
df5 = pd.DataFrame(SupplierToProduct)

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
                                     supplier_id int(11) NOT NULL,
                                     nb_followers int(11) NOT NULL,
                                     Name varchar(250) NOT NULL,
                                     store_no varchar(250) NOT NULL,
                                     country varchar(250) NOT NULL,
                                     opening_date date NOT NULL,
                                     PRIMARY KEY (supplier_id)) """

        mySql_Create_Table_Query2 = """
        CREATE TABLE if not exists Product(
                                     product_id int(11) NOT NULL, 
                                     title varchar(250) NOT NULL,
                                     delivery varchar(250) NOT NULL,
                                     Price float NOT NULL,
                                     quantity_sold int(11) NOT NULL,
                                     rating int(11) NOT NULL,
                                     store varchar(250) NOT NULL,
                                     discount int(11) NOT NULL,
                                     available_quantity int(11) NOT NULL,
                                     PRIMARY KEY (product_id)) """


        mySql_Create_Table_Query3 = """
        CREATE TABLE if not exists Product_specifications(  
                                     product_id int(11) NOT NULL,
                                     Brand_Name VARCHAR(250) NOT NULL,
                                     Video_Memory_Capacity int(11) NOT NULL,
                                     Interface_Type VARCHAR(250) NOT NULL,
                                     Cooler_Type VARCHAR(250) NOT NULL,
                                     Stream_Processors int(11) NOT NULL,
                                     Chip_Process VARCHAR(250) NOT NULL,
                                     Model_Number VARCHAR(250) NOT NULL,
                                     PixelPipelines int(11) NOT NULL,
                                     Launch_Date DATE NOT NULL,
                                     Output_Interface_Type1 VARCHAR(250) NOT NULL,
                                     Output_Interface_Type2 VARCHAR(250) NOT NULL,
                                     Memory_Interface VARCHAR(250) NOT NULL,
                                     PRIMARY KEY (product_id),
                                     FOREIGN KEY (product_id) REFERENCES Product(product_id)) """

        mySql_Create_Table_Query4 = """
        CREATE TABLE if not exists Reviews(
                                     review_id INT NOT NULL, 
                                     product_id INT NOT NULL,
                                     country VARCHAR(200),
                                     stars INT NOT NULL,
                                     is_image BOOL NOT NULL,
                                     useful_yes INT NOT NULL,
                                     useful_no INT NOT NULL,
                                     date DATE NOT NULL,
                                     text VARCHAR(500),
                                     FOREIGN KEY (product_id) REFERENCES Product(product_id),                                     
                                     PRIMARY KEY (review_id)) """

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
        result3 = cursor.execute(mySql_Create_Table_Query3)
        result4 = cursor.execute(mySql_Create_Table_Query4)
        result5 = cursor.execute(mySql_Create_Table_Query5)

        sql_str1 = "INSERT INTO Supplier (supplier_id, nb_followers, Name, store_no, country, opening_date) VALUES (%s, %s, %s, %s, %s, %s)"

        sql_str2 = "INSERT INTO Product (product_id, title, delivery, Price, quantity_sold, rating, store, discount, available_quantity)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        sql_str3 = "INSERT INTO Product_specifications (product_id, Brand_Name, Video_Memory_Capacity, Interface_Type, Cooler_Type, Stream_Processors, Chip_Process, Model_Number, PixelPipelines, Launch_Date, Output_Interface_Type1, Output_Interface_Type2, Memory_Interface) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        sql_str4 = "INSERT INTO Reviews (review_id, product_id, country, stars, is_image, useful_yes, useful_no, date, text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        sql_str5 = "INSERT INTO SupplierToProduct (SupplierToProduct_id, supplier_id, product_id) VALUES (%s, %s, %s)"

        cursor.executemany(sql_str1, df1.values.tolist())
        cursor.executemany(sql_str2, df2.values.tolist())
        cursor.executemany(sql_str3, df3.values.tolist())
        cursor.executemany(sql_str4, df4.values.tolist())
        cursor.executemany(sql_str5, df5.values.tolist())

        connection.commit()

        print("Tables created successfully ")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")