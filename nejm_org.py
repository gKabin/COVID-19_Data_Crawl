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

pages = np.arange(1, 6)

for page in pages: 
    
    page = requests.get("https://www.nejm.org/search?q=sars-cov-2&asug=#qs=%3Fq%3Dsars-cov-2%26requestType%3Dajax%26asug%3D%26viewClass%3D%26page%3D"+str(pages)+"%26manualFilterParam%3DcontentAge_delimiter_contentAge_delimiter_contentAge_delimiter_contentAge_firstDelimiter")
    
    soup = BeautifulSoup(page.text, 'html.parser')
    covid19_article = soup.find_all('li', class_='m-result')
    
    sleep(randint(2,10))
    
    for n in np.arange(0, 20):

        # Getting the title
        title = covid19_article[n].find('strong', class_ = 'm-result__title f-h4').get_text()
        list_titles.append(title)
        
        #Getting authors
        authors = covid19_article[n].find('em', class_ = 'm-result__author f-author').get_text()
        list_authors.append(authors)
        
        #Getting DOI
        doi = covid19_article[n].find('em', class_ = 'm-result__publisher f-author').get_text()
        list_doi.append(doi)
        
        #Getting the published date
        dates = covid19_article[n].find('em', class_ = 'm-result__date f-tag').get_text()
        list_dates.append(dates)
        
        # Getting the link of the article
        site = "https://www.nejm.org"
        site1 = covid19_article[n].find('a', class_ = 'js__sliLearn m-result__link')['href']
        link = site + site1
        list_links.append(link)
        
        #Getting abstracts
        abstracts = covid19_article[n].find('span', class_ = 'm-result__blurb f-blurb').get_text()
        list_abstracts.append(abstracts)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_dates,
     'Link': list_links,
     'Abstracts': list_abstracts})

print(df_show_info)