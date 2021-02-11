import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import regex as re
import requests
import openpyxl

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

city = 'santaclarita' #*****change this city to what you want*****
pages = 10 #***** set to the number of pages to scrape + 1

#create a master and page dataframe
df = pd.DataFrame()
df_master = pd.DataFrame()

for page in range(1, pages):
    with requests.Session() as s:
       url = 'https://www.zillow.com/homes/for_sale/'+city+"/"+str(page)+"_p/"
       print(url)
       r = s.get(url, headers=req_headers)

    #add contents of urls to soup variable from each url
    soup = BeautifulSoup(r.content, 'html.parser')

    #Create lists to store the values
    price_list = []
    address_list = []
    bed_list = []
    br_list = []
    sqft_list = []
    prop_list = []

    #pull variables based on class (where possible). These lists contain html tags
    price_list_soup = soup.find_all (class_='list-card-price')
    address_list_soup = soup.find_all (class_= 'list-card-addr')

    #Use text function to remove tags.
    for element in price_list_soup:
        price_list.append(element.text)
    for element in address_list_soup:
        address_list.append(element.text)

    #The details variables are all listed under a single class. Parse conents in 'list-card-details' class
    for ul_tag in soup.find_all("ul", class_="list-card-details"):
        li_tag = list(ul_tag.find_all('li'))
        #Void data if property does not have a completed details field.
        if len(li_tag) != 4:
            bed_list.append("N/A")
            br_list.append("N/A")
            sqft_list.append("N/A")
            prop_list.append("N/A")
            continue
        #extract number of beds
        beds = li_tag.pop(0).text
        beds = beds[:-1]
        bed_list.append(beds)
        #extract number of bathrooms
        bathrooms = li_tag.pop(0).text
        bathrooms = bathrooms[:-1]
        br_list.append(bathrooms)
        #extract sqft
        sqft = li_tag.pop(0).text
        sqft = sqft[:-1]
        sqft_list.append(sqft)
        #extract property type
        prop_type = li_tag.pop(0).text
        prop_type = prop_type.split("- ")[1].split(" ")[0]
        prop_list.append(prop_type)

    #create dataframe columns out of variables
    df['prices'] = price_list
    df['address'] = address_list
    df['beds'] = bed_list
    df['bathrooms'] = br_list
    df['square ft'] = sqft_list
    df['prop_type'] = prop_list

    #create empty url list
    urls = []

    #loop through url, pull the href and strip out the address tag
    for link in soup.find_all("article"):
        href = link.find('a',class_="list-card-link")
        addresses = href.find('address')
        addresses.extract()
        urls.append(href)#import urls into a links column
    df['links'] = urls
    df['links'] = df['links'].astype('str')#remove html tags
    df['links'] = df['links'].replace('<a class="list-card-link list-card-link-top-margin" href="', ' ', regex=True)
    df['links'] = df['links'].replace('" tabindex="0"></a>', ' ', regex=True)

    df_master = df_master.append(df, ignore_index = True)

df_master.to_excel("ZillowScrape.xlsx", sheet_name = city)
