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
import re

req_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.5',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0'
}

with requests.Session() as s:
   url = 'https://www.zillow.com/homedetails/27578-Cobblestone-Ct-Valencia-CA-91354/65251480_zpid/'
   r = s.get(url, headers=req_headers)

#add contents of urls to soup variable from each url
soup = BeautifulSoup(r.content, 'html.parser')

listing_details = soup.find(class_="ds-home-fact-list")
print(listing_details.prettify)
listing_details_dict = {}
categories = []
values =[]
i = 1
for detail in listing_details.find_all(class_=re.compile("Text-c11n-8-18-0__aiai24-0")):
    if i % 2 != 0:
        categories.append(detail.text)
    else:
        values.append(detail.text)
    i += 1
listing_details_dict = dict(zip(categories, values))
print(listing_details_dict)

#for category in listing_details.find_all(class_=re.compile("Text-c11n-8-18-0__aiai24-0 sc-")):
#    print(category.text)
#    categories.append(category.text)
#for value in listing_details.find_all(class_=re.compile("Text-c11n-8-18-0__aiai24-0 foiYRz"):
#    categories.append(category.text)
#listing_details_dict = dict(zip(categories, values))
#print(listing_details_dict)

#title = soup.find(class_="Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 efSAZl")
#cost_details = soup.find("div", class_="ds-expandable-card undefined")
#print(cost_details.prettify)
#cost_categories = []
#costs =[]
#for category in cost_details.find_all(class_="Text-c11n-8-18-0__aiai24-0 iuVuVk"):
#    cost_categories.append(category.text)
#for cost in cost_details.find_all(class_="Text-c11n-8-18-0__aiai24-0 cNBYuL"):
#    costs.append(cost.text)
#cost_details_dict = dict(zip(cost_categories, costs))
#print(cost_details_dict)
