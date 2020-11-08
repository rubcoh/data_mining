import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import requests
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import random

proxies = ['157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128', '157.230.247.57:3128']

PROXY = '157.230.247.57:3128'
webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,

    "proxyType": "MANUAL",
}

def switch_proxy(proxies):
    number = random.randint(0, len(proxies) - 1)
    PROXY = proxies[number]
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }
    print(F"Proxy switched to {PROXY}")


options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7")
options.headless = False
options.add_argument("--disable-notifications")

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


DRIVER_PATH = "/Users/ruben/Desktop/Softwares/chromedriver"
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


titles = ['Titles']
delivery = ['Delivery']
prices = ['Prices']
qty_sold = ['Quantity sold']
ratings = ['Ratings']
stores = ['Stores']

titles_path = ']/div/div[2]/div/div[1]/a'
delivery_path = ']/div/div[2]/div/div[3]/span'
prices_path = ']/div/div[2]/div/div[2]/div[1]/span'
qty_sold_path = ']/div/div[2]/div/div[7]/div/span/a'
ratings_path = ']/div/div[2]/div/div[7]/a/span'
stores_path =']/div/div[2]/div/div[8]/a'


def get_data(my_path, my_list):
    switch_proxy(proxies)
    WEBSITE_PATH = "https://fr.aliexpress.com/category/205006047/cellphones.html"
    driver.maximize_window()
    driver.get(WEBSITE_PATH)
    for pages in range(1, 2):
        try:
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[2]/div/a"))).click()
        except Exception:
            pass
        for row in range(1, 13):
            for col in range(1, 6):
                try:
                    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/ul/div[' + str(row) + ']/li[' + str(col) + my_path)))
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    my_list.append(element.text)
                    print(f"Found element {row}X{col} of page {pages} while scraping {my_list[0]}")
                except Exception:
                    print(f"Couldn't find element {row}X{col} of page {pages} while scraping {my_list[0]}")
                    break
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]'))).click()




get_data(titles_path, titles)
time.sleep(random.randint(1, 2))
get_data(delivery_path, delivery)
#time.sleep(random.randint(1, 2))
#get_data(prices_path, prices)
#time.sleep(random.randint(1, 2))
#get_data(qty_sold_path, qty_sold)
#time.sleep(random.randint(1, 2))
#get_data(ratings_path, ratings)
#time.sleep(random.randint(1, 2))
#get_data(stores_path, stores)



print(titles)
print(delivery)
#print(prices)
#print(qty_sold)
#print(ratings)
#print(stores)
print(len(titles))
print(len(delivery))

df = pd.DataFrame(titles, delivery)
print(df)