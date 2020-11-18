from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from time import sleep
import requests
import datetime
import json 

# Global try except in case something goes wrong

try: 

    # Define our variables

    titleList = []
    priceList = []
    URLList = []
    imgList = []
    cpt = 0
    data = []

    #  Function to display the exact time 

    def displayTime():
        now = datetime.datetime.now()
        return("["+now.strftime("%Y-%m-%d %H:%M:%S")+"] ")

    # Function to add data to JSON 

    def write_json(data, filename='deals.json'): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 


    #  Set the query and number of pages to scroll

    query = str(input('What are you looking for ? '))
    pages = str(input('How many pages should we crawl ? '))

    #  Set the user agent

    ua = UserAgent().random

    # Define webdriver options 

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1400,600')
    options.add_argument("user-agent="+str(ua))


    #  Launching webdriver

    print(displayTime()+"Launching ...")

    driver = webdriver.Chrome(options=options)

    #  Set the URL and send request



    for i in range (1,int(pages)+1) :

        if(i==1) :

            url = 'https://www.amazon.fr/s?k='+query 

        else :

            url = 'https://www.amazon.fr/s?k='+'query+&page='+str(i)

        driver.get(url)

        #  Sleep

        sleep(2)

        #  Get source code

        response = driver.page_source

        if(i==1) :

            print(displayTime()+"HTTP 200 OK - Connection Established")

        

        #  Scrape the data


        page = BeautifulSoup(response, 'html.parser')



        #  Get each product

        products = page.select('div.sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.s-result-item.s-asin.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32')

        for product in products :


            # condition to get rid of any product that doesn't display a price

            if(product.find('span',{'class':'a-price-whole'})) :
                
                #  Get the titles

                titles = product.select('span.a-size-base-plus.a-color-base.a-text-normal')
                prices = product.select('span.a-price-whole')
                URLs = product.select('a.a-link-normal.s-no-outline')
                imgs = product.select('img.s-image')

                # Display each title

                for title in titles :
                    titleList.append(title.text)
                
                for price in prices :
                    priceList.append(price.text)
                
                for URL in URLs :
                    URLList.append('https://amazon.fr'+URL['href'])

                for img in imgs :
                    imgList.append(img['src'])
                

            # If the price is not displayed we get rid of it 

            else : 
                pass

            
        print(displayTime()+'Page '+str(i)+' Retrieved')


        


    # Collect all the data in a JSON format

    for title in titleList :

        # Replace commas by dots for better number comprehension

        priceList[cpt] = priceList[cpt].replace(',','.')

        data.append({

                'title' : title,
                'price' : float(priceList[cpt]),
                'URL' : URLList[cpt],
                'img' : imgList[cpt]

            })
            
        cpt+=1



    # Reorder the data by price


    temp = sorted(data, key=lambda k: k['price']) 


    data = temp



    # Insert all the data to JSON File
        
    write_json(data) 

    # Print the results

    print(displayTime()+'Finished !'+"\n")

except :

    # Error message in case it doesn't work

    print(displayTime()+'An error has occured ...')

        