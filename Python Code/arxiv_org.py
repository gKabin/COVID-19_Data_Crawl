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
pages_urls = []

#Parsing URL function
def getAndParseURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return(soup)

#Getting Page URLs
new_page = "https://arxiv.org/search/?query=sars-cov-2&searchtype=all&source=header&start=0"

while True:
    soup = getAndParseURL(new_page)
    covid19 = soup.find_all('li', class_='arxiv-result')
    article_num = len(covid19)
    if (requests.get(new_page).status_code == 200 and article_num > 0):
        i = len(pages_urls)
        pages_urls.append(new_page)
        new_page = pages_urls[i].split("start=")[0] + "start=" + str(int(pages_urls[i].split("start=")[1]) + 50)
    else:
        break
        
#Getting articles content
for url in pages_urls:    
    soup = getAndParseURL(url)   
    covid19 = soup.find_all('li', class_='arxiv-result')
    
    article_num = len(covid19)
    for n in np.arange(0, article_num):
        
        #Getting the title
        title = covid19[n].find('p', class_ = 'title is-5 mathjax').get_text()
        trim_title = title.strip()
        list_title.append(trim_title)

        #Getting the link of the article
        link = covid19[n].find('p', class_ = 'list-title is-inline-block').a['href']
        list_links.append(link)

        #Getting authors
        covid19_author = soup.find_all('p', class_='authors')
        author_num = covid19_author[0].find_all('a')
        list_author = []
        for a in np.arange(0, len(author_num)):
            author = author_num[a].get_text()
            list_author.append(author)
            authors = ", ".join(list_author)
        list_authors.append(authors)

        #Getting doi
        doi = covid19[n].find('div', class_ = "is-marginless").p.a.get_text()
        list_doi.append(doi)

        #Getting abstract
        abstract = covid19[n].find('span', class_ = 'abstract-full has-text-grey-dark mathjax').get_text()
        trim_abstract = abstract.strip() 
        list_abstract.append(trim_abstract.split("\n", 1)[0])
        
        #Getting Published date
        date = covid19[n].find('p', class_ = 'is-size-7').get_text()
        trim_date = date[date.find("Submitted") + 10 : date.find("; ")]
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

end_time = time.time()
print("--- Execution time is: %.2f seconds ---" % (end_time - start_time))

print(df_show_info)