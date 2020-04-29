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
list_keywords = []
pages_urls = []

#Parsing URL function
def getAndParseURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return(soup)

#Getting Page URLs
new_page = "https://emeraldopenresearch.com/search?q=covid-19&show=30&page=1"

while True:
    soup = getAndParseURL(new_page)
    covid19 = soup.find_all('div', class_='article-title-text')
    article_num = len(covid19)
    if (requests.get(new_page).status_code == 200 and article_num > 0):
        i = len(pages_urls)
        pages_urls.append(new_page)
        new_page = pages_urls[i].split("page=")[0] + "page=" + str(int(pages_urls[i].split("page=")[1]) + 1)
    else:
        break

#Getting articles content
for url in pages_urls:    
    soup = getAndParseURL(url)   
    covid19 = soup.find_all('div', class_='article-title-text')
    covid19_date = soup.find_all('div', class_ = 'article-bottom-bar')
    covid19_author = soup.find_all('div', class_ = 'article-detail-text')
    
    article_num = len(covid19)

    for n in np.arange(0, article_num):

        # Getting the title
        title = covid19[n].a.span.get_text()
        list_titles.append(title)

        # Getting the link of the article
        link = covid19[n].find('a', class_='article-link')['href']
        list_links.append(link)

        #Getting the published date
        date = covid19_date[n].get_text()
        trim_date = date[date.find("PUBLISHED ") + 10 : date.find("0\n") +1]
        list_dates.append(trim_date)
        
        #Getting authors
        author_num = covid19_author[n].find_all('span')
        list_author = []
        for a in np.arange(0, len(author_num)):
            author = author_num[a].get_text()
            trim_author = author.strip()
            list_author.append(trim_author)
            authors = " ".join(list_author)
        list_authors.append(authors)

        #Reading article content
        soup_data = getAndParseURL(link)
        covid19_doi = soup_data.find_all('span', 'info-separation padding-bottom')

        #Getting abstract
        abstract = soup_data.find('div', class_='abstract-text is-expanded').get_text()
        list_abstract.append(abstract)

        #Getting DOI
        doi = covid19_doi[1].find('a').get_text()
        trim_doi = doi.split("doi.org/", 1)
        list_doi.append(trim_doi[1])

        #Getting Keywords
        keywords = soup_data.find('div', class_='article-abstract article-page-general-text-mobile research-layout generated-article-body').p.get_text()
        list_keywords.append(keywords)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_dates,
     'Keywords' : list_keywords,
     'Link': list_links,
     'Abstracts': list_abstract
    })

end_time = time.time()
print("--- Execution time is: %.2f seconds ---" % (end_time - start_time))

print(df_show_info)