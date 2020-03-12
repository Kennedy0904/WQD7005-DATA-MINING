#!/usr/bin/env python
# coding: utf-8

# ### Milestone 1: Web Scrapping
# WQD180102 Ng Wei Xin <br>
# WQD180104 Tan Bing Shien

# In[ ]:


# pip install requests
# pip install beautifulsoup4

import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# using requests to fetch pages
# Note: Python Selenium library can be used for javascript pages (by imitating browser behaviour)

# bs4: Html-Parser (or XML), to navigate through html documents


# In[ ]:


# Get url content using python-requests
page = requests.get('https://www.thestar.com.my/news/latest')
contents = page.content

# Parse html document in bs4
soup = BeautifulSoup(contents, 'html.parser')
print(soup.prettify())


# In[ ]:


# Create empty dict
# Note: using news-id as identifier -> prevent duplication
myList = {}

# Use class "timeline-content" to identify news section
for tag in soup.find_all(class_= "timeline-content", limit=15):

    # Further navigate to "h2" tag
    for subtag in tag.find('h2'):
        
        # Get String (news headline), trim / strip linebreaks
        strNews = "".join(line.strip() for line in subtag.string.split("\n"))
        idNews = "".join(line.strip() for line in subtag['data-content-id'].split("\n"))
        
        # Crawl sub page, get Date / Timestamp
        newsHref = subtag['href']
        subPage = requests.get(newsHref)
        subContent = subPage.content
        subSoup = BeautifulSoup(subContent, 'html.parser')
        timeTag = "".join(line.strip() for line in subSoup.find('time', {'class': 'timestamp'}).string.split("\n"))
        dateTag = "".join(line.strip() for line in subSoup.find('p', {'class': 'date'}).string.split("\n"))
        
        # (print) News-ID: News-String
        print("News-ID ("+idNews+"):")
        print(strNews)
        print(newsHref)
        print(dateTag)
        print(timeTag)
        print()
        
        # Add entry to list 
        myList[subtag['data-content-id']]=strNews


# In[ ]:


def recrawl(objDF):
    page = requests.get('https://www.thestar.com.my/news/latest')
    contents = page.content

    soup = BeautifulSoup(contents, 'html.parser')

    for tag in soup.find_all(class_= "timeline-content", limit = 15):
        for subtag in tag.find('h2'):
            
            # News-ID
            idNews = "".join(line.strip() for line in subtag['data-content-id'].split("\n"))
                        
            # Check for duplication, proceed only for new item
            # else skip to save computation
            if not df['News_ID'].str.contains(idNews).any():
                
                # Headline
                strNews = "".join(line.strip() for line in subtag.string.split("\n"))
                
                # Category
                catNews = "".join(line.strip() for line in subtag['data-content-category'].split("\n"))
                
                # Timestamp (spider on respective news page)
                newsHref = subtag['href']
                subPage = requests.get(newsHref)
                subContent = subPage.content
                subSoup = BeautifulSoup(subContent, 'html.parser')
                dateNews = "".join(line.strip() for line in subSoup.find(class_="date").string.split("\n"))
                timeNews = "".join(line.strip() for line in subSoup.find(class_="timestamp").string.split("\n"))
                
                # Add info to list
                objDF = objDF.append(pd.Series([idNews, dateNews, timeNews, catNews, strNews, newsHref], index=objDF.columns), ignore_index=True)

    return objDF


# In[ ]:


# Create Empty DataFrame:
df= pd.DataFrame(columns=["News_ID", "Date", "Timestamp", "Category", "Headline", "URL"])

# Endless-Loop
# while True: 
    
i = 1 # Test: using 3 counts 
while i>0:
    
    df = recrawl(df)
    print(df)
    
    # Export dataframe to csv file
    df.to_csv(r'C:\Users\FORGE-15 I7\OneDrive - AsiaPay Limited\Sem 3\WQD7005 DATA MINING\dataset.csv', index = False)
#     df.to_csv(r'C:\Users\ngwei\Desktop\dataset.csv', index = False)
    
    i=i-1
    #time.sleep(300) # Re-Crawl every 5 minutes


# In[ ]:


# save to csv
# df.to_csv(r'C:\Users\ngwei\Desktop\dataset.csv', index = False)


# # Save scraped content into a txt file

# file1 = open("tmpcrawl.txt","w") 

# # file1.write("Hello \n") 
# # file1.write(str(soup.prettify())) 
# file1.write(str(myList)) 

# file1.close() 

