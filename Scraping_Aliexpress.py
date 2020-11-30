"""
This program is a web scraper for the website Aliexpress.com.
It allows to retrieve data on prices, titles, shipping, quantity sold, ratings and sellers or smartphones.
"""

# Here are the packages that we use in our program
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import argparse



# Here we import the config file
import my_config as CFG

# Here is a list of proxies on which we switch regularly
proxies = CFG.PROXIES

# Here we set our browser preferences and options
options = Options()
# Here we setup a user-agent
options.add_argument(CFG.USER_AGENT_PATH)

# Here we decide whether if we run the program headless or not
options.headless = CFG.HEADLESS
# Here we disable notifications
options.add_argument(CFG.DISABLE_NOTIFICATIONS)
# Here we disable pictures display
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)

options.add_argument(CFG.INCOGNITO)

# Here we setup the webdriver with all the previous options
#### REPLACE THIS PATH BY YOUR THE PATH OF WEBDRIVER ON YOUR COMPUTER ####
DRIVER_PATH = CFG.DRIVER_PATH
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


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





def get_specific_data(my_path, my_list, nb_pages, identifier):
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
    #switch_proxy(proxies)
    # Here is the path of the page on which we want to scrape data
    WEBSITE_PATH = "https://fr.aliexpress.com/premium/category/205006120.html?CatId=205006120"
    # Here we maximize the window to display and scrape more content
    driver.maximize_window()
    # Here we go to the home page
    driver.get(WEBSITE_PATH)


    products = ['titles', 'delivery', 'prices', 'qty_sold', 'ratings', 'stores', 'discounts']
    suppliers = ['nb_followers', 'name', 'store_no', 'supplier_country', 'opening_date']
    reviews = ['reviews_1_stars', 'reviews_2_stars', 'reviews_3_stars', 'reviews_4_stars', 'reviews_5_stars']
    p = driver.current_window_handle
    driver.switch_to.window(p)

    #driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
    for pages in range(1, nb_pages + 1):
        time.sleep(3)
        driver.refresh()
        try:
            # Here we close the popup appearing at each opening or refresh of a page
            close_popup = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/"
                                                                                                "div[2]/div/a")))
            close_popup.click()
        except TimeoutException:
            pass

        # The items are displayed in a grid of 12 rows and 5 columns
        for row in range(1, 3):
            for col in range(1, 3):

                if identifier in suppliers or identifier in reviews:

                    try:
                        # Click on the picture of the product
                        time.sleep(2)
                        button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                                                                             '//*[@id="root"]/div/div/'
                                                                                             'div[2]/div[2]/div/div[2]/'
                                                                                             'ul/div[' + str(
                                                                                                 row) + ']/li[' + str(
                                                                                                 col) + "]/div/div[1]/"
                                                                                                        "div/a/img")))
                        # driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        button.click()
                        time.sleep(2)
                    except Exception:
                        print(f"Couldn't find product picture {row}X{col}")


                    # get first child window
                    chwd = driver.window_handles

                    for w in chwd:
                        # switch focus to child window
                        if (w != p):
                            driver.switch_to.window(w)

                    try:
                        time.sleep(3)
                        driver.refresh()
                        # Here we close the popup appearing at each opening or refresh of a page
                        close_popup = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='3607353940']/div/div/img")))
                        close_popup.click()
                    except TimeoutException:
                        pass

                    if identifier in suppliers:
                        try:
                            element_to_hover = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='store-info-wrap']/div[1]/h3/a")))
                            hover = ActionChains(driver).move_to_element(element_to_hover)
                            hover.perform()
                        except Exception:
                            print(f"Unable to hover while scraping {identifier}")


                try:
                    if identifier in suppliers or identifier in reviews:
                        element = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, my_path)))
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(3)
                        my_list.append(element.text)

                    elif identifier in products:
                        element = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                                                                              '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/ul/div[' + str(row) + ']/li[' + str(col) + my_path)))
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(3)
                        my_list.append(element.text)
                        time.sleep(3)
                        my_list.append(element.text)
                    print(f"Found element {row}X{col} of page {pages} while scraping {identifier}")
                    print("The element is", element.text)
                except Exception:
                    print(f"Couldn't find element {row}X{col} of page {pages} while scraping {identifier}")
                    my_list.append(None)

                if identifier in suppliers or identifier in reviews:

                    #driver.close()
                    driver.switch_to.window(p)

                    time.sleep(3)
                    driver.refresh()
                    try:
                        # Here we close the popup appearing at each opening or refresh of a page
                        close_popup = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/"
                                                                  "div[2]/div/a")))
                        close_popup.click()
                    except TimeoutException:
                        pass

            driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

        time.sleep(5)
        try:
            # Here we go to the next page
            page_number = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div/div/button[' + str(pages) + ']')))
            #driver.execute_script("arguments[0].scrollIntoView(true);", page_number)
            page_number.click()
        except Exception:
            print("Couldn't reach the page button")
            break



def scrape_store(nb_pages, is_titles=False, is_delivery=False, is_prices=False, is_qty_sold=False, is_ratings=False,
                 is_stores=False, is_discounts=False, is_nb_followers = False, is_name = False, is_store_no = False,
                 is_supplier_country = False, is_opening_date = False, is_reviews_1_stars=False, is_reviews_2_stars=False,
                 is_reviews_3_stars=False, is_reviews_4_stars=False, is_reviews_5_stars=False):


    # Here we initialize a list for each type of data we want to scrape on the website

    # Product
    titles = []
    delivery = []
    prices = []
    qty_sold = []
    ratings = []
    stores = []
    discounts = []

    # Supplier
    nb_followers = []
    name = []
    store_no = []
    supplier_country = []
    opening_date = []

    """
    # Product specifications
    brand_name = []
    video_memory_capacity = []
    interface_type = []
    cooler_type = []
    stream_processors = []
    chip_process = []
    model_number = []
    pixel_pipelines = []
    launch_date = []
    output_interface_type1 = []
    output_interface_type2 = []
    memory_interface = []
    """

    # Reviews
    reviews_1_stars = []
    reviews_2_stars = []
    reviews_3_stars = []
    reviews_4_stars = []
    reviews_5_stars = []



    # Here are the variable part of each xpath on which we will loop to obtain each item of the website

    # Product
    TITLES_PATH = ']/div/div[2]/div/div[1]/a'
    DELIVERY_PATH = ']/div/div[2]/div/div[3]/span'
    PRICES_PATH = ']/div/div[2]/div/div[2]/div[1]/span'
    QTY_SOLD_PATH = ']/div/div[2]/div/div[7]/div/span/a'
    RATINGS_PATH = ']/div/div[2]/div/div[7]/a/span'
    STORES_PATH = ']/div/div[2]/div/div[8]/a'
    DISCOUNTS_PATH = ']/div/div[2]/div/div[2]/div[2]/span[2]'

    # Supplier
    NB_FOLLOWERS_PATH = '//*[@id="store-info-wrap"]/div[2]/p/i'
    NAME_PATH = '//*[@id="store-info-wrap"]/div[1]/h3/a'
    STORE_NO_PATH = '//*[@id="store-dsr-balloon-tips"]/div/div/div/div[1]/span[1]'
    SUPPLIER_COUNTRY_PATH = '//*[@id="store-dsr-balloon-tips"]/div/div/div/div[1]/span[2]'
    OPENING_DATE_PATH = '//*[@id="store-dsr-balloon-tips"]/div/div/div/div[1]/span[3]/em'
    """
    # Product specifications
    BRAND_NAME_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[1]/span[2]'
    VIDEO_MEMORY_CAPACITY_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[23]/span[2]'
    INTERFACE_TYPE_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[14]/span[2]'
    COOLER_TYPE_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[15]/span[2]'
    STREAM_PROCESSORS_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[2]/span[2]'
    CHIP_PROCESS_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[12]/span[2]'
    MODEL_NUMBER_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[21]/span[2]'
    PIXEL_PIPELINES_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[4]/span[2]'
    LAUNCH_DATE_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[6]/span[2]'
    OUTPUT_INTERFACE_TYPE1_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[16]/span[2]'
    OUTPUT_INTERFACE_TYPE2_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[18]/span[2]'
    MEMORY_INTERFACE_PATH = '//*[@id="product-detail"]/div[2]/div/div[2]/div[4]/div/ul/li[7]/span[2]'
    """


    # Reviews
    REVIEW_1_STARS_PATH = '//*[@id="transction-feedback"]/div[2]/ul/li[5]/span[3]'
    REVIEW_2_STARS_PATH = '//*[@id="transction-feedback"]/div[2]/ul/li[4]/span[3]'
    REVIEW_3_STARS_PATH = '//*[@id="transction-feedback"]/div[2]/ul/li[3]/span[3]'
    REVIEW_4_STARS_PATH = '//*[@id="transction-feedback"]/div[2]/ul/li[2]/span[3]'
    REVIEW_5_STARS_PATH = '//*[@id="transction-feedback"]/div[2]/ul/li[1]/span[3]'




    IMAGE_PATH = ']/div/div[1]/div/a/img'

    #Here we run the get_general_data() function on each kind of items we want to scrape from the website

    len_product = 0
    len_supplier = 0
    #len_specification = 0
    len_reviews = 0

    if is_titles:
        get_specific_data(TITLES_PATH, titles, nb_pages, 'titles')
        len_product = len(titles)

    if is_delivery:
        get_specific_data(DELIVERY_PATH, delivery, nb_pages, 'delivery')
        len_product = len(delivery)

    if is_prices:
        get_specific_data(PRICES_PATH, prices, nb_pages, 'prices')
        len_product = len(prices)

    if is_qty_sold:
        get_specific_data(QTY_SOLD_PATH, qty_sold, nb_pages, 'qty_sold')
        len_product = len(qty_sold)

    if is_ratings:
        get_specific_data(RATINGS_PATH, ratings, nb_pages, 'ratings')
        len_product = len(ratings)

    if is_stores:
        get_specific_data(STORES_PATH, stores, nb_pages, 'stores')
        len_product = len(stores)

    if is_discounts:
        get_specific_data(DISCOUNTS_PATH, discounts, nb_pages, 'discounts')
        len_product = len(discounts)

    if is_nb_followers:
        get_specific_data(NB_FOLLOWERS_PATH, nb_followers, nb_pages, 'nb_followers')
        len_supplier = len(nb_followers)


    if is_name:
        get_specific_data(NAME_PATH, name, nb_pages, 'name')
        len_supplier = len(name)


    if is_store_no:
        get_specific_data(STORE_NO_PATH, store_no, nb_pages, 'store_no')
        len_supplier = len(store_no)


    if is_supplier_country:
        get_specific_data(SUPPLIER_COUNTRY_PATH, supplier_country, nb_pages, 'supplier_country')
        len_supplier = len(supplier_country)


    if is_opening_date:
        get_specific_data(OPENING_DATE_PATH, opening_date, nb_pages, 'is_opening_date')
        len_supplier = len(opening_date)


   ############################################################################################
   ############################################################################################
    """
    if is_brand_name:
        get_specific_data(BRAND_NAME_PATH, brand_name, nb_pages, 'brand_name')
        len_specification = len(brand_name)

    if is_video_memory_capacity:
        get_specific_data(VIDEO_MEMORY_CAPACITY_PATH, video_memory_capacity, nb_pages, 'video_memory_capacity')
        len_specification = len(video_memory_capacity)

    if is_interface_type:
        get_specific_data(INTERFACE_TYPE_PATH, interface_type, nb_pages, 'interface_type')
        len_specification = len(interface_type)

    if is_cooler_type:
        get_specific_data(COOLER_TYPE_PATH, cooler_type, nb_pages, 'cooler_type')
        len_specification = len(cooler_type)

    if is_stream_processors:
        get_specific_data(STREAM_PROCESSORS_PATH, stream_processors, nb_pages, 'stream_processors')
        len_specification = len(stream_processors)

    if is_chip_process:
        get_specific_data(CHIP_PROCESS_PATH, chip_process, nb_pages, 'chip_process')
        len_specification = len(chip_process)

    if is_model_number:
        get_specific_data(MODEL_NUMBER_PATH, model_number, nb_pages, 'model_number')
        len_specification = len(model_number)

    if is_pixel_pipelines:
        get_specific_data(PIXEL_PIPELINES_PATH, pixel_pipelines, nb_pages, 'pixel_pipelines')
        len_specification = len(pixel_pipelines)

    if is_launch_date:
        get_specific_data(LAUNCH_DATE_PATH, launch_date, nb_pages, 'launch_date')
        len_specification = len(launch_date)

    if is_output_interface_type1:
        get_specific_data(OUTPUT_INTERFACE_TYPE1_PATH, output_interface_type1, nb_pages, 'output_interface_type1')
        len_specification = len(output_interface_type1)

    if is_output_interface_type2:
        get_specific_data(OUTPUT_INTERFACE_TYPE2_PATH, output_interface_type2, nb_pages, 'output_interface_type2')
        len_specification = len(output_interface_type2)

    if is_memory_interface:
        get_specific_data(MEMORY_INTERFACE_PATH, memory_interface, nb_pages, 'memory_interface')
        len_specification = len(memory_interface)
    """

    if is_reviews_1_stars:
        get_specific_data(REVIEW_1_STARS_PATH, reviews_1_stars, nb_pages, 'reviews_1_stars')
        len_reviews = len(reviews_1_stars)

    if is_reviews_2_stars:
        get_specific_data(REVIEW_2_STARS_PATH, reviews_2_stars, nb_pages, 'reviews_2_stars')
        len_reviews = len(reviews_2_stars)

    if is_reviews_3_stars:
        get_specific_data(REVIEW_3_STARS_PATH, reviews_3_stars, nb_pages, 'reviews_3_stars')
        len_reviews = len(reviews_3_stars)

    if is_reviews_4_stars:
        get_specific_data(REVIEW_4_STARS_PATH, reviews_4_stars, nb_pages, 'reviews_4_stars')
        len_reviews = len(reviews_4_stars)

    if is_reviews_5_stars:
        get_specific_data(REVIEW_5_STARS_PATH, reviews_5_stars, nb_pages, 'reviews_5_stars')
        len_reviews = len(reviews_5_stars)








    products = [titles, delivery, prices, qty_sold, ratings, stores, discounts]
    suppliers = [nb_followers, name, store_no, supplier_country, opening_date]
    reviews = [reviews_1_stars, reviews_2_stars, reviews_3_stars, reviews_4_stars, reviews_5_stars]


    PRODUCTS_SIZE = len_product
    for item in products:
        if len(item) < 2:
            item = np.empty(PRODUCTS_SIZE)
            item[:] = None
            item.tolist()

    SUPPLIER_SIZE = len_supplier
    for item in suppliers:
        if len(item) < 2:
            item = np.empty(SUPPLIER_SIZE)
            item[:] = None
            item.tolist()

    REVIEWS_SIZE = len_reviews
    for item in reviews:
        if len(item) < 2:
            item = np.empty(REVIEWS_SIZE)
            item[:] = None
            item.tolist()


    # Finally, we create a pandas dataframe with the lists we created and we store it into a csv file

    dict_product = {
            'titles': np.array(titles),
            'delivery': np.array(delivery),
            'prices': np.array(prices),
            'qty_sold': np.array(qty_sold),
            'ratings': np.array(ratings),
            'stores': np.array(stores),
            'discounts': np.array(discounts)
            }

    df_product = pd.DataFrame.from_dict(dict_product, orient='index')
    df_product = df_product.transpose()


    dict_supplier = {
            'nb_followers': np.array(nb_followers),
            'name': np.array(name),
            'store_no': np.array(store_no),
            'supplier_country': np.array(supplier_country),
            'opening_date': np.array(opening_date),

            }

    df_supplier = pd.DataFrame.from_dict(dict_supplier, orient='index')
    df_supplier = df_supplier.transpose()

    """
    dict_specification = {
            'brand_name': np.array(brand_name),
            'video_memory_capacity': np.array(video_memory_capacity),
            'interface_type': np.array(interface_type),
            'cooler_type': np.array(cooler_type),
            'stream_processors': np.array(stream_processors),
            'chip_process': np.array(chip_process),
            'model_number': np.array(model_number),
            'pixel_pipelines': np.array(pixel_pipelines),
            'launch_date': np.array(launch_date),
            'output_interface_type1': np.array(output_interface_type1),
            'output_interface_type2': np.array(output_interface_type2),
            'memory_interface': np.array(memory_interface),
            }

    df_specification = pd.DataFrame.from_dict(dict_specification, orient='index')
    df_specification = df_specification.transpose()

    """

    dict_reviews = {
                'reviews_1_stars': np.array(reviews_1_stars),
                'reviews_2_stars': np.array(reviews_2_stars),
                'reviews_3_stars': np.array(reviews_3_stars),
                'reviews_4_stars': np.array(reviews_4_stars),
                'reviews_5_stars': np.array(reviews_5_stars),

                }

    df_reviews = pd.DataFrame.from_dict(dict_reviews, orient='index')
    df_reviews = df_reviews.transpose()





    random_number = np.random.randint(1, 1000000)
    df_product.to_csv("products_" + str(random_number) + ".csv")
    df_supplier.to_csv("suppliers_" + str(random_number) + ".csv")
    df_reviews.to_csv("reviews" + str(random_number) + ".csv")
    print(df_product)
    print(df_supplier)
    print(df_reviews)



is_titles = False
is_prices = False
is_delivery = False
is_qty_sold = False
is_ratings = False
is_stores = False
is_discounts = False

is_nb_followers = False
is_name = False
is_store_no = False
is_supplier_country = False
is_opening_date = False

is_reviews_1_stars = False
is_reviews_2_stars = False
is_reviews_3_stars = False
is_reviews_4_stars = False
is_reviews_5_stars = False

my_parser = argparse.ArgumentParser(description="""This is a Command line interface """)
my_parser.add_argument('--nb_pages', help='number of pages to scrap', type=int, required=True)
my_parser.add_argument('--Product_Table', help='Scrap Product Table', type=bool, required=False)
my_parser.add_argument('--Reviews_Table', help='Scrap Reviews Title', type=bool, required=False)
my_parser.add_argument('--Supplier_Table', help='Scrap Supplier Table', type=bool, required=False)
args = my_parser.parse_args()

if args.Product_Table == True:
    is_titles = True
    is_prices = True
    is_delivery = True
    is_qty_sold = True
    is_ratings = True
    is_stores = True
    is_discounts = True
if args.Supplier_Table == True:
    is_nb_followers = True
    is_name = True
    is_store_no = True
    is_supplier_country = True
    is_opening_date = True
if args.Reviews_Table == True:
    is_reviews_1_stars = True
    is_reviews_2_stars = True
    is_reviews_3_stars = True
    is_reviews_4_stars = True
    is_reviews_5_stars = True


scrape_store(args.nb_pages, is_titles, is_delivery, is_prices, is_qty_sold, is_ratings,
                 is_stores, is_discounts, is_nb_followers, is_name, is_store_no,
                 is_supplier_country, is_opening_date, is_reviews_1_stars, is_reviews_2_stars, is_reviews_3_stars,
             is_reviews_4_stars ,is_reviews_5_stars)

