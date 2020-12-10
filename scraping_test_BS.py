from bs4 import BeautifulSoup
import requests




WEBSITE_PATH = "https://fr.aliexpress.com/category/205006047/cellphones.html"

website = requests.get(WEBSITE_PATH)
main_content = website.content
soup = BeautifulSoup(main_content,'lxml')

products = ['titles', 'delivery', 'prices', 'qty_sold', 'ratings', 'stores', 'discounts']
suppliers = ['nb_followers', 'name', 'store_no', 'supplier_country', 'opening_date']
reviews = ['reviews_1_stars', 'reviews_2_stars', 'reviews_3_stars', 'reviews_4_stars', 'reviews_5_stars']

links = []

#print(soup.find_all('iframe'))
#for element in soup.find_all('div'):
    #for url in soup.find_all('div', {"class": 'product-img'}):
        #for link in url.find_all('a'):
        #    links.append(link.attrs['href'])
#        print(element)


#print(main_content)
#print(links)


for content in soup.find('body').find('iframe'):
    print(content)



#for frame in content.find('iframe'):
#   links.append(frame.attrs['src'])


