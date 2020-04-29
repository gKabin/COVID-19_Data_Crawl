import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time

start_time = time.time()

headers = {"Accept-Language": "en-US,en;q=0.5"}

list_title = []
list_authors = []
list_doi = []
list_date = []
list_links = []
list_abstract = []
list_keywords = []
pages_urls = []

# Parsing URL function
def getAndParseURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return(soup)

# Getting Page URLs
new_page = "https://www.preprints.org/search?search1=sars-cov-2&field1=title_keywords&field2=authors&clause=AND&page_num=1"

while True:
    soup = getAndParseURL(new_page)
    covid19 = soup.find_all('div', class_='search-content-box margin-serach-wrapper-left')
    article_num = len(covid19)
    if (requests.get(new_page).status_code == 200 and article_num > 0):
        i = len(pages_urls)
        pages_urls.append(new_page)
        new_page = pages_urls[i].split("page_num=")[0] + "page_num=" + str(int(pages_urls[i].split("page_num=")[1]) + 1)
    else:
        break
        
# Getting articles content
for url in pages_urls:    
    
    soup = getAndParseURL(url)   
    covid19 = soup.find_all('div', class_='search-content-box margin-serach-wrapper-left')
    
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

        # Getting authors
        authors = covid19[n].find('div', class_ = 'search-content-box-author').get_text()
        trim_authors = authors.strip()
        list_authors.append(trim_authors)
        
        # Getting doi
        doi = covid19[n].find('a').get_text()
        trim_doi = doi[doi.find(":")+1 : doi.find("\ ")]
        list_doi.append(trim_doi)
        
        # Getting abstracts
        abstract = covid19[n].find('div', class_ = 'abstract-content').get_text()
        trim_abstract = abstract.strip()
        list_abstract.append(trim_abstract)
        
        # Getting Published date
        date = covid19[n].find('div', class_ = 'show-for-large-up').get_text()
        trim_date = date[date.find(": ")+1 : date.find("(")]
        list_date.append(trim_date)

        trye = covid19[n].find_all('div')
    
        # Getting Published date
        keywords = trye[4].get_text()
        trim_keywords = keywords.split('Keywords: \n', 1)
        list_keywords.append(trim_keywords[1])

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_title,
     'Authors': list_authors,
     'DOI': list_doi,
     'Keywords' : list_keywords,
     'Published Date': list_date,
     'Link': list_links,
     'Abstracts': list_abstract
    })

end_time = time.time()
print("--- Execution time is: %.2f seconds ---" % (end_time - start_time))

print(df_show_info)