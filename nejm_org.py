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
list_abstract = []

pages = np.arange(1, 8)

url = "https://www.nejm.org/search?q=sars-cov-2&asug=#qs=%3Fq%3Dsars-cov-2%26requestType%3Dajax%26asug%3D%26viewClass%3D%26page%3D"+str(pages)+"%26manualFilterParam%3DcontentAge_delimiter_contentAge_delimiter_contentAge_delimiter_contentAge_firstDelimiter"

for page in pages: 
    
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, 'html.parser')
    covid19 = soup.find_all('li', class_='m-result')

    sleep(randint(2,10))
    
    article_num = len(covid19)

    for n in np.arange(0, article_num):

        # Getting the title
        title = covid19[n].find('strong', class_ = 'm-result__title f-h4').get_text()
        list_titles.append(title)

        #Getting the published date
        dates = covid19[n].find('em', class_ = 'm-result__date f-tag').get_text()
        list_dates.append(dates)

        # Getting the link of the article
        site = "https://www.nejm.org"
        get_href = covid19[n].find('a', class_ = 'js__sliLearn m-result__link')['href']
        link = site + get_href
        list_links.append(link)
        
        # Getting DOI
        doi = get_href.split("full/", 1)
        list_doi.append(doi[1])
        
        # Reading the content
        article = requests.get(link)
        article_content = article.text
        soup_data = BeautifulSoup(article_content, 'html.parser')
        covid19_author = soup_data.find_all('ul', class_='m-article-header__authors f-ui')
        covid19_abstract = soup_data.find_all('section', class_='o-article-body__section')

        #Getting authors
        author_num = covid19_author[0].find_all('li')
        list_author = []
        for a in np.arange(0, len(author_num)):
            author = author_num[a].get_text()
            list_author.append(author)
            authors = " ".join(list_author)
        list_authors.append(authors)

        #Getting abstracts
        para_num = covid19_abstract[0].find_all('p')
        list_paragraphs = []
        for p in np.arange(0, len(para_num)):
            paragraph = para_num[p].get_text()
            list_paragraphs.append(paragraph)
            abstract = " ".join(list_paragraphs)
        list_abstract.append(abstract)

#df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Authors': list_authors,
     'DOI': list_doi,
     'Published Date': list_dates,
     'Link': list_links,
     'Abstracts': list_abstract})

print(df_show_info)