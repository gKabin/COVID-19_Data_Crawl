import requests
from requests import get
import feedparser
import numpy as np
import time


#Parsing URL function
def getAndParseURL(url):
    data = feedparser.parse(url)
    return(data)

def crawl():
    start_time = time.time()

    headers = {"Accept-Language": "en-US,en;q=0.5"}

    list_titles = []
    list_authors = []
    list_doi = []
    list_dates = []
    list_links = []
    list_abstract = []
    list_keywords = []
    json_abstract = []


    new_page = "https://connect.biorxiv.org/relate/feed/181"

    #Getting article contents
    # soup = getAndParseURL(new_page)
    soup = feedparser.parse(new_page)
    article = soup['entries']

    for n in np.arange(0, len(article)):
            
            #Getting the title
            title = article[n].title.strip()
            list_titles.append(title)
            
            #Getting the link of the article
            link = article[n].link.strip()
            trim_link = link.split('?rss=1', 1)
            list_links.append(trim_link[0])
            
            #Getting Published date
            date = article[n].date.strip()
            list_dates.append(date)
            
            #Getting DOI
            doi = article[n].dc_identifier.strip()
            trim_doi = doi.split(":", 1)
            list_doi.append(trim_doi[1])
            
            #Getting abstract
            abstract = article[n].description.strip()
            list_abstract.append(abstract)
            
            #Getting authors
            author_num = article[n].authors
            list_author = []
            for a in np.arange(0, len(author_num)):
                list_author.append(author_num[a].get('name', ''))
                authors = ";".join(list_author)
            list_authors.append(authors)

            json_abstract.append({
                'title': title,
                'url': trim_link,
                'authors': authors,
                'doi': doi,
                'abstract': abstract,
                'date': date
            })
    end_time = time.time()
    print("--- Execution time is: %.2f seconds ---" % (end_time - start_time))        
    return json_abstract

print(crawl())
