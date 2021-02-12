from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

city = input("Enter a city: ").replace(" ", "")
pages = int(input("Enter the number of pages to scrape: "))

#create a master and page dataframe
df = pd.DataFrame()
df_master = pd.DataFrame()

for page in range(1, pages + 1):
    with requests.Session() as s:
       url = 'https://www.zillow.com/homes/for_sale/'+city+"/"+str(page)+"_p/"
       print(url)
       r = s.get(url, headers=req_headers)

    #add contents of urls to soup variable from each url
    soup = BeautifulSoup(r.content, 'html.parser')

    #Create lists to store the values
    url_list = []
    price_list = []
    address_list = []
    bed_list = []
    br_list = []
    sqft_list = []
    prop_list = []

    #pull variables based on class (where possible).
    for link in soup.find_all("a", class_="list-card-link list-card-link-top-margin"):
        url_list.append(link.get("href"))
    for price in soup.find_all (class_='list-card-price'):
        price_list.append(price.text)
    for address in soup.find_all (class_= 'list-card-addr'):
        address_list.append(address.text)

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
    df['links'] = url_list

    df_master = df_master.append(df, ignore_index = True)

df_master.to_excel("ZillowScrape.xlsx", sheet_name = city)
