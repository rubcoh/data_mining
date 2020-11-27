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
    'text': str(i*'ab')
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