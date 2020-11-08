####  AIiExpres Product Data Scraper

### Purpose
# ITC Data mining project- first checkpoint

### abstract 
# Product page scraping module.
# we have created a Product Data Scraper in Python code using Selenium (a portable framework for testing web applications).

### Usage
# insert into script:
# url = 'https://aliexpress.com/category/some_catagory_number/some_product.html'
# driver = "Directory location of your chrome webdriver exe"
# this will create a csv file with the info of the product

### Flow of the scrapper:
# 1- Go to AIiExpress product url
# 2- Close the sales pop up
# 3- Take the product info from each product on the current page: matrix of (12, 6)
# => see data specifics on the next paragraph 
# 4- Go to the next page by click on the next page number
# 5- Create a data frame with all the scrapped data
# 6- Create a csv from the information

### Data
# The data scrapper has the following product info: (arranged into a pandas data frame)
# Titles: name of the product
# Delivery: time till Delivery: 
# Prices: The price of the product
# Quantity sold: how much products of the same kind were sold on the site
# Ratings: The review rate given by the consumers 
# Stores: What online stores sell this product

### challenges
# Restriction and blockings: (multiple automated requests), 
# first we used several proxies servers (A proxy server masks the true origin of the request to the resource server).
# However, proxy servers were not enough and we therefore used also different user agents -
# a software agent that operates in a network protocols, it identifies itself, its application type, operating system, software vendor, or software revision, 
# by submitting a number characteristic identification string to its operating peer. 
# we used a python package to help us send different user agents each time we scrapped the data from the website

# Slowness in page rendering: due to many resources usage (many open chrome windows),
# this caused an issue where we wanted to scrap an element from a page but couldn't because the page wasn't loaded yet,
# then this raised an exception of NoSuchElementException. 
# we dealt with the mater by providing time.sleep() and WebDriverWait which provided the page with opportunity to load the elements to the page before running the script.

### Requiments:
# pip installs:
# pandas==1.1.3
# selenium==3.141.0
# download, unzip and install ChromeDriver - WebDriver: (more info below)
# [https://sites.google.com/a/chromium.org/chromedriver/downloads]

### Contact
# Created by Ruben Cohen & Yaniv Weiss - feel free to contact us.





 
