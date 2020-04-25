import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US,en;q=0.5"}

list_titles = []
list_authors = []
list_doi = []
list_dates = []
list_links = []
list_abstracts = [] 

pages = np.arange(1, 50)

for page in pages: 
    
    page = requests.get("https://connect.biorxiv.org/relate/content/181?page=" + str(page) + " ")
    
    soup = BeautifulSoup(page.text, 'html.parser')    
    covid19 = soup.find_all('div', class_='highwire-article-citation highwire-citation-type-highwire-article')
    doi_date = soup.find_all('div', class_ = 'highwire-cite-metadata')
    
    sleep(randint(2,10))
    
    article_num = len(covid19)

    for n in np.arange(0, article_num):
        
        # Getting the title
        title = covid19[n].find('span', class_ = 'highwire-cite-title').a.get_text()
        list_titles.append(title)

        #Getting doi and published date
        doi_dates = doi_date[n].find('span', class_ = 'highwire-cite-metadata-journal').get_text()
        new_doi_dates = doi_dates.split(" — Posted: ", 1)
        list_doi.append(new_doi_dates[0])
        list_dates.append(new_doi_dates[1])

        # Getting the link of the article
        link = covid19[n].find('a', class_ = 'highwire-cite-linked-title')['href']
        list_links.append(link)
        
        # Reading the content
        article = requests.get(link)
        article_content = article.text
        soup_data = BeautifulSoup(article_content, 'html.parser')
        covid19_article = soup_data.find_all('div', class_='panel-pane pane-highwire-article-citation')
        covid19_abstract = soup_data.find_all('div', class_='article abstract-view')

        #Getting authors
        authors = covid19_article[1].find('span', class_ = 'highwire-citation-authors').get_text()
        list_authors.append(authors)

        #Getting abstracts
        abstracts = covid19_abstract[0].find('div', class_ = 'section abstract').p.get_text()
        list_abstracts.append(abstracts)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_dates,
     'Link': list_links,
     'Abstracts': list_abstracts
    })

print(df_show_info)