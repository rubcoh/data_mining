import json
import requests
import pandas as pd

import my_config as CFG

api_key = CFG.API_KEY

def read_file(file_name):
    with open(file_name, 'r') as read_file:
        data = json.load(read_file)
        print(f'Successfully read {file_name}')
    return  data

def save_file(data, file_name):
    with open(file_name, 'w') as write_file:
        json.dump(data, write_file, indent=4)
        print(f'Successfully saved {file_name}')

#Top stories
def get_top_articles():
    url = f'https://api.nytimes.com/svc/topstories/v2/arts.json?api-key=' + api_key
    response = requests.get(url).json()
    save_file(response, 'response.json')
    read_file('response.json')
    return response

#Most viewed, shared, or emailed articles
def get_most_popular_articles():
    url2 = f'https://api.nytimes.com/svc/topstories/v2/arts.json?api-key=' + api_key
    response = requests.get(url2).json()
    save_file(response_most_pop, 'most_pop.json')
    read_file('most_pop.json')
    return response


get_top_articles()

f = open('response.json',)

data = json.load(f)

df = pd.json_normalize(data, 'results', ['section', 'subsection', 'title'], errors='ignore', record_prefix='results_')


df.to_csv('/Users/ruben/Documents/ITC/Data_mining_project/nyt_text.csv')