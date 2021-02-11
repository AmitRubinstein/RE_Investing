import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re
import requests
import lxml
from lxml.html.soupparser import fromstring
import prettify
import numbers
import htmltext

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

with requests.Session() as s:
   city = 'santaclarita/' #*****change this city to what you want*****
   url = 'https://www.zillow.com/homes/for_sale/'+city
   r = s.get(url, headers=req_headers)

#add contents of urls to soup variable from each url
soup = BeautifulSoup(r.content, 'html.parser')
bed_list = []
br_list = []
sqft_list = []
prop_list = []
counter = 0
for results in soup:
    if counter < 2:
        for ul_tag in soup.find_all("ul", class_="list-card-details"):
            li_tag = list(ul_tag.find_all('li'))
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
    counter = counter + 1

#print(bed_list)
#print(br_list)
#print(sqft_list)
print(prop_list)
