import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
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
    soup = BeautifulSoup(page.text, 'lxml-xml')
    return(soup)

new_page = "https://connect.biorxiv.org/relate/feed/181"

#Getting article contents
soup = getAndParseURL(new_page)
article = soup.find_all('item')

for n in np.arange(0, len(article)):
        
        #Getting the title
        title = article[n].title.text.strip()
        list_titles.append(title)
        
        #Getting the link of the article
        link = article[n].link.text.strip()
        trim_link = link.split('?rss=1', 1)
        list_links.append(trim_link[0])
        
        #Getting Published date
        date = article[n].date.text.strip()
        list_dates.append(date)
        
        #Getting DOI
        doi = article[n].identifier.text.strip()
        trim_doi = doi.split(":", 1)
        list_doi.append(trim_doi[1])
        
        #Getting abstract
        abstract = article[n].description.text.strip()
        list_abstract.append(abstract)
        
        #Getting authors
        author_num = article[n].find_all('creator')
        list_author = []
        for a in np.arange(0, len(author_num)):
            author = author_num[a].get_text()
            #trim_author = author.strip()
            list_author.append(author)
            authors = ";".join(list_author)
        list_authors.append(authors)

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