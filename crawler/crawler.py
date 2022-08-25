from bs4 import BeautifulSoup
import requests
import time as time 
import random
import pandas as pd
import utils 
import pickle as pkl
from decouple import config
import json

# set variables
user_agents = []
with open('crawler/uas_list', 'rb') as f:
      uas = pkl.load(f)
      user_agents.extend(uas)

user_agent = random.choice(user_agents)

#container
main_lst = []

def crawl(search_text:str) -> dict:

      for page_num in range(int(config('max_pages'))):
            
            time.sleep(3)

            # format input search keyword to match URL search
            search = utils.format_search_text(search_text)
            base_url = 'https://scholar.google.com'
            search_url = f'https://scholar.google.com/scholar?start={page_num}0&q={search}&hl=en&scisbd=2&as_sdt=0,5&as_rr=1'

            # browser headers
            headers = {
                  "Referer" : "https://scholar.google.com/scholar?start=20&q=school+students&hl=en&as_sdt=0,5&as_rr=1",
                  "User-Agent" : user_agent
            }

            # request response
            response = requests.get(search_url, headers=headers)
            print(response.status_code)

            # parse response content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract required data
            articles = soup.findAll('div', {'class':'gs_scl'})
            for article in articles:
                 
                  post_date_str = article.find('span', {'class':'gs_age'}).get_text()
                  item = {
                  "title" : article.find('h3', {'class':'gs_rt'}).get_text().replace('\n', '').strip(),
                  "link" : str(article.find('a', href=True)['href']).strip(),
                  "author" : article.find('div', {'class':'gs_a'}).get_text().replace('\n', '').strip(),
                  "post_date" : utils.time_post(post_date_str),
                  "summary" : article.find('div', {'class':'gs_rs'}).get_text().replace(post_date_str,'').replace('\n', '').strip()
                  }
                  main_lst.append(item)
            print(f'done for {page_num}')

      return main_lst

# filter user requirements
def dyn_crawl(keyword:str, no_articles: int = config('max_articles'), links:bool=True, author:bool=True, summary:bool=True):
      
      # crawl data
      result = crawl(keyword)

      # filter no of articles output 
      defined_result = result[:no_articles]

      # if links==False:
      #       no_link = [x.pop("link") for x in defined_result]
            
      # if author==False:
      #       no_author = [x.pop("author") for x in defined_result]

      # if summary==False:
      #       no_summary = [x.pop("summary") for x in defined_result]

      
      return defined_result

