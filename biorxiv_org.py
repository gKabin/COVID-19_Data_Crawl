import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time

start_time = time.time()

headers = {"Accept-Language": "en-US,en;q=0.5"}

list_titles = []
list_authors = []
list_doi = []
list_dates = []
list_links = []
list_abstract = []

# Parsing URL function
def getAndParseURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return(soup)

pages = np.arange(1, 10)

for page in pages: 
    
    #Parsing Pages URL
    main_url = "https://connect.biorxiv.org/relate/content/181?page=" + str(page) + " "
    soup = getAndParseURL(main_url) 
    
    covid19 = soup.find_all('div', class_='highwire-article-citation highwire-citation-type-highwire-article')
    doi_date = soup.find_all('div', class_ = 'highwire-cite-metadata')
    
    #Getting Article Contents
    article_num = len(covid19)
    for n in np.arange(0, article_num):
        
        #Getting the title
        title = covid19[n].find('span', class_ = 'highwire-cite-title').a.get_text()
        list_titles.append(title)

        #Getting doi and published date
        doi_dates = doi_date[n].find('span', class_ = 'highwire-cite-metadata-journal').get_text()
        new_doi_dates = doi_dates.split(" — Posted: ", 1)
        list_doi.append(new_doi_dates[0])
        list_dates.append(new_doi_dates[1])

        #Getting the link of the article
        link = covid19[n].find('a', class_ = 'highwire-cite-linked-title')['href']
        list_links.append(link)
        
        #Parsing Article URL
        soup_data = getAndParseURL(link)
        covid19_article = soup_data.find_all('div', class_='panel-pane pane-highwire-article-citation')
        covid19_abstract = soup_data.find_all('div', class_='article abstract-view')

        #Getting authors
        authors = covid19_article[1].find('span', class_ = 'highwire-citation-authors').get_text()
        list_authors.append(authors)

        #Getting abstract
        abstract = covid19_abstract[0].find('div', class_ = 'section abstract').p.get_text()
        list_abstract.append(abstract)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_dates,
     'Link': list_links,
     'Abstract': list_abstract
    })

end_time = time.time()
print("--- Execution time is: %.2f seconds ---" % (end_time - start_time))

print(df_show_info)