#  AIiExpres Product Data Scraper

## Purpose
###### ITC Data mining project- second checkpoint

## Abstract 
######  Product page scraping module.
######  We have created a Product Data Scraper in Python code using Selenium (a portable framework for testing web applications).
######  We added a command-line interface that allows the user to define the tables that he wants to scrape as well as the number of pages to scrape.
######  We also added a configuration file that allows to define the navigation parameters (proxies, user-agents, incognito mode..)
######  The data scraped is then inserted into a database that was created using MySQL. 
######  An ERD of the data scraped is also available in the repository.
## Usage
###### Open the file Scraping_Aliexpress.py
###### Insert into the Python script:
######  - driver = "Directory location of your chrome webdriver exe"
###### Then from the command line, input:
###### '--nb_pages': (INT) to define the number of pages to scrape
###### '--Product_Table': (BOOL) to allow the scraping of the 'Products' table
###### '--Product_Spec_Table': (BOOL) to allow the scraping of the 'Specifications' table
###### '--Supplier_Table': (BOOL) to allow the scraping of the 'Suppliers' table
###### EXAMPLE:
###### "(base) C:\Users\yaniv\PycharmProjects\data_mining>python commandline.py --nb_pages 3 --Product_Table 1 --Product_Spec_Table 1"
###### Connect to your database as follows:
###### "connection = mysql.connector.connect(host='your_localhost', database='database_name', user='root', password='your_password')
###### Change parameters from the config file
###### In order to insert the data scraped, run mysql_code.py 
## Flow of the scrapper:
###### 1- The scrapper goes to AliExpress product url
###### 2- It scrapes items (example: product title) one by one depending on the user's choice. 
###### 3- Each item is put under the form of a list containing all the products data for this specific item.
###### 4- All the obtained lists are gathered as columns of Dataframes, each Dataframe representing a future table of our database.
###### 5- Each Dataframe is saved as a csv file.

## Data
    # Product table
    titles = title/name of the product
    delivery = shipping cost
    prices = price of the product
    qty_sold = quantity already sold of the product
    ratings = rating of the product
    stores = supplier which sells the product
    discounts = discount on the product (if applicable)

    # Supplier table
    nb_followers = number of followers of the supplier
    name = name of the supplier
    store_no = store number of the supplier
    supplier_country = country of the supplier
    opening_date = opening date of the supplier

    # Product specifications table
    brand_name = brand name of the GPU
    video_memory_capacity = video memory capacity of the GPU
    interface_type = interface type of the GPU
    cooler_type = cooler type of the GPU
    stream_processors = stream processors of the GPU
    chip_process = chip process of the GPU
    model_number = model number of the GPU
    pixel_pipelines = pixel pipelines of the GPU
    launch_date = launch date of the GPU
    output_interface_type1 = output interface 1 of the GPU
    output_interface_type2 = output interface 2 of the GPU
    memory_interface = memory interface of the GPU

## challenges
###### Restriction and blockings: (multiple automated requests), 
###### first we used several proxies servers (A proxy server masks the true origin of the request to the resource server).
###### However, proxy servers were not enough and we therefore used also different user agents -
###### a software agent that operates in a network protocols, it identifies itself, its application type, operating system, software vendor, or software revision, 
###### by submitting a number characteristic identification string to its operating peer. 
###### we used a python package to help us send different user agents each time we scrapped the data from the website

###### Slowness in page rendering: due to many resources usage (many open chrome windows),
###### this caused an issue where we wanted to scrap an element from a page but couldn't because the page wasn't loaded yet,
###### then this raised an exception of NoSuchElementException. 
###### we dealt with the mater by providing time.sleep() and WebDriverWait which provided the page with opportunity to load the elements to the page before running the script.

## Requiments:

###### pip installs:
###### pandas==1.1.3
###### selenium==3.141.0
###### mysql==0.0.2
###### mysql-connector-python==8.0.22
###### requests==2.24.0
###### download, unzip and install ChromeDriver - WebDriver: (more info below)
###### [https://sites.google.com/a/chromium.org/chromedriver/downloads]

## Contact
###### Created by Ruben Cohen & Yaniv Weiss - feel free to contact us.

