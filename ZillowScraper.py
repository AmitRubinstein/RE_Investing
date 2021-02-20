from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl
import re

def SearchResultsScrape (req_headers):
    #Solicit user input
    city = input("Enter a city: ").replace(" ", "")
    pages = int(input("Enter the number of pages to scrape: "))

    #create a master and page dataframe to collect data
    df = pd.DataFrame()
    df_master = pd.DataFrame()

    #iterate through search result pages
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
        street_list = []
        city_list = []
        state_list = []
        zip_list = []
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
            #Split address into individual fields
            zip = address.text[-5:]
            street, city, state = address.text.split(", ")
            state = state[:2]
            #assign address fields to lists
            street_list.append(street)
            city_list.append(city)
            state_list.append(state)
            zip_list.append(zip)

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
        df["Hyperlink"] = url_list
        df["Address"] = address_list
        df["Street"] = street_list
        df["City"] = city_list
        df["State"] = state_list
        df["Zip Code"] = zip_list
        df["Price"] = price_list
        df["# Bedrooms"] = bed_list
        df["# Bathrooms"] = br_list
        df["Sq Feet"] = sqft_list
        df["Property Type"] = prop_list


        #append dataframe for current page to master dataframe
        df_master = df_master.append(df, ignore_index = True)

    return df_master

def ListingScrape(req_headers,df):
    #create lists to store the values for DF
    HOA_list = []
    #create loop to iterate through the listings
    for index, row in df.iterrows():
        url = row["Hyperlink"]
        #prep the soup
        with requests.Session() as s:
            print(url)
            r = s.get(url, headers=req_headers)
            soup = BeautifulSoup(r.content, 'html.parser')
        # Get HTML
        listing_details = soup.find(class_="ds-home-fact-list")
        #Create lists to store values in listing details
        categories = []
        values =[]
        listing_details_dict = {}
        #Collect listing details
        i = 1
        for detail in listing_details.find_all(class_=re.compile("Text-c11n-8-18-0__aiai24-0")):
            if i % 2 != 0:
                categories.append(detail.text)
            else:
                values.append(detail.text)
            i += 1
            listing_details_dict = dict(zip(categories, values))
        #Store values for DF from listing details in a list
        if "HOA:" in listing_details_dict:
            HOA_list.append(listing_details_dict.get("HOA:"))
        else:
            HOA_list.append("")
    df["HOA"] = HOA_list
    return df



def main():
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    df1 = SearchResultsScrape(req_headers)
    df2 = ListingScrape(req_headers, df1)
    df2.to_excel("ZillowScrape.xlsx")

if __name__ == "__main__":
    main()
