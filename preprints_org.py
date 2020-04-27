import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US,en;q=0.5"}

list_title = []
list_authors = []
list_doi = []
list_date = []
list_links = []
list_abstract = []

pages = np.arange(1, 8)

for page in pages:    
    
    page = requests.get("https://www.preprints.org/search?search1=sars-cov-2&field1=title_keywords&field2=authors&clause=AND&page_num=" + str(page) + " ")
    
    soup = BeautifulSoup(page.text, 'html.parser')    
    covid19 = soup.find_all('div', class_='search-content-box margin-serach-wrapper-left')
    
    sleep(randint(2,10))
    
    article_num = len(covid19)

    for n in np.arange(0, article_num):
        
        # Getting the title
        title = covid19[n].find('a', class_ = 'title').get_text()
        list_title.append(title)

        # Getting the link of the article
        site = "https://www.preprints.org"
        link = covid19[n].find('a', class_ = 'title')['href']
        url = site + link
        list_links.append(url)

        #Getting authors
        authors = covid19[n].find('div', class_ = 'search-content-box-author').get_text()
        trim_authors = authors.strip()
        list_authors.append(trim_authors)
        
        #Getting doi
        doi = covid19[n].find('a').get_text()
        trim_doi = doi[doi.find(":")+1 : doi.find("\ ")]
        list_doi.append(trim_doi)
        
        #Getting abstracts
        abstract = covid19[n].find('div', class_ = 'abstract-content').get_text()
        trim_abstract = abstract.strip()
        list_abstract.append(trim_abstract)
        
        #Getting Published date
        date = covid19[n].find('div', class_ = 'show-for-large-up').get_text()
        trim_date = date[date.find(": ")+1 : date.find("(")]
        list_date.append(trim_date)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_title,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_date,
     'Link': list_links,
     'Abstracts': list_abstract
    })

print(df_show_info)