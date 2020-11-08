"""
This program is a web scraper for the website Aliexpress.com.
It allows to retrieve data on prices, titles, shipping, quantity sold, ratings and sellers or smartphones.
"""

# Here are the packages that we use in our program
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options
import time
import requests
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Here is a list of proxies on which we switch regularly
proxies = ['157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128',
           '157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128']

def switch_proxy(proxies):
    """
    This function switches randomly from one proxy to another, given a list of proxies.
    :param proxies:
    :return: new random proxy
    """

    # Generates a random index
    number = random.randint(0, len(proxies) - 1)
    # Randomly selects a proxy in the proxy list
    PROXY = proxies[number]
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    print(f"Proxy switched to {PROXY}")


# Here we set our browser preferences and options
options = Options()
# Here we setup a user-agent
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7")
# Here we decide whether if we run the program headless or not
options.headless = False
# Here we disable notifications
options.add_argument("--disable-notifications")
# Here we disable pictures display
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


# Here we setup the webdriver with all the previous options
#### REPLACE THIS PATH BY YOUR THE PATH OF WEBDRIVER ON YOUR COMPUTER ####
DRIVER_PATH = "/Users/ruben/Desktop/Softwares/chromedriver"
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# Here we initialize a list for each type of data we want to scrape on the website
titles = ['Titles']
delivery = ['Delivery']
prices = ['Prices']
qty_sold = ['Quantity sold']
ratings = ['Ratings']
stores = ['Stores']

# Here are the variable part of each xpath on which we will loop to obtain each item of the website
TITLES_PATH = ']/div/div[2]/div/div[1]/a'
DELIVERY_PATH = ']/div/div[2]/div/div[3]/span'
PRICES_PATH = ']/div/div[2]/div/div[2]/div[1]/span'
QTY_SOLD_PATH = ']/div/div[2]/div/div[7]/div/span/a'
RATINGS_PATH = ']/div/div[2]/div/div[7]/a/span'
STORES_PATH =']/div/div[2]/div/div[8]/a'


def get_data(my_path, my_list, nb_pages):
    """
    Given a variable part of xpath, a list and a number of pages, this function allows to fill the list with data
    scraped from the Aliexpress.com smartphones pages.
    We used sleep times regularly to wait for the data to load and to maje the behavior of the code more human-like.
    :param my_path:
    :param my_list:
    :param nb_pages:
    :return: None
    """
    # Here we switch proxy
    switch_proxy(proxies)
    # Here is the path of the page on which we want to scrape data
    WEBSITE_PATH = "https://fr.aliexpress.com/category/205006047/cellphones.html"
    # Here we maximize the window to display and scrape more content
    driver.maximize_window()
    # Here we go to the home page
    driver.get(WEBSITE_PATH)

    for pages in range(1, nb_pages + 1):
        time.sleep(1)
        try:
            # Here we close the popup appearing at each opening or refresh of a page
            close_popup = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[2]/div/a")))
            close_popup.click()
        except TimeoutException:
            pass
        # The items are displayed in a grid of 12 rows and 5 columns
        for row in range(1, 13):
            for col in range(1, 6):
                try:
                    # Here we scrape the data following a grid of items on the page (nb_rows X nb_columns) and append each element to a list
                    element = WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/ul/div[' + str(row) + ']/li[' + str(col) + my_path)))
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    my_list.append(element.text)
                    print(f"Found element {row}X{col} of page {pages} while scraping {my_list[0]}")
                except Exception:
                    print(f"Couldn't find element {row}X{col} of page {pages} while scraping {my_list[0]}")
                    my_list.append(None)
        time.sleep(2)
        try:
            # Here we go to the next page
            page_number = WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div/div/button[' + str(pages) + ']')))
            page_number.click()
        except Exception:
            print("Couldn't reach the page button")
            break


#Here we run the get_data() function on each kind of items we want to scrape from the website
NB_PAGES = 1

get_data(TITLES_PATH, titles, NB_PAGES)
get_data(DELIVERY_PATH, delivery, NB_PAGES)
get_data(PRICES_PATH, prices, NB_PAGES)
get_data(QTY_SOLD_PATH, qty_sold, NB_PAGES)
get_data(RATINGS_PATH, ratings, NB_PAGES)
get_data(STORES_PATH, stores, NB_PAGES)

# Finally, we create a pandas dataframe with the lists we created and we store it into a csv file
df = pd.DataFrame(
    {'titles': titles,
     'delivery': delivery,
     'prices': prices,
    'qty_sold': qty_sold,
    'ratings': ratings,
    'stores': stores,
    })

#### REPLACE THIS PATH BY THE PATH WHERE YOU WANT TO SAVE THE FILE ####
df.to_csv("/Users/ruben/Desktop/df.csv")
print(df)