from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
import sys



def webcrawler(location, checkin, checkout):
    hnames = []
    hlocations = []
    hdist = []
    hprice = []
    hcomments = []
    hrating = []
    
    chrome_options = Options()

    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()
    
    url = f'https://www.booking.com/searchresults.en-us.html?ss={location}&checkin={checkin}&checkout={checkout}'

    driver.get(url)


    try:
        accept = '//*[@id="onetrust-accept-btn-handler"]'
        accept_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, accept)))
        accept_button.click()
        page_source = driver.page_source
    except:
        page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    pages = soup.find_all('button', class_='a83ed08757 a2028338ea')
    pagenum = []
    for page in pages:
        pagenum.append(int(page.text))

    maxpagenum = np.max(pagenum)

    properties = soup.find_all('div', {'class': 'c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4', 'data-testid':'property-card'})
    for k, property in enumerate(properties):
        names = property.find('div', {'class':'f6431b446c a15b38c233', 'data-testid':'title'})
        locations = property.find('span', {'class':'aee5343fdb def9bc142a', 'data-testid':'address'})
        distances = property.find('span',{'data-testid':"distance"})
        rating = property.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
        price = property.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f', 'data-testid':"price-and-discounted-price"})
        comments = property.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
        if names == None:
            names = []
            
            hnames.append(np.nan)
        if locations == None:
            locations = []
            
            hlocations.append(np.nan)
        if distances == None:
            distances = []
           
            hdist.append(np.nan)
        if rating == None:
            rating = []
            
            hrating.append(np.nan)
        if price == None:
            price = []
            
            hprice.append(np.nan)
        if comments == None:
            comments = []
            
            hcomments.append(np.nan)

        for element in names:
            hnames.append(element.text)
            
        for element in locations:
            hlocations.append(element.text)
            
        for element in distances:
            dist = float(element.text.split(' ')[0])
            if dist>99.9:
                dist = dist/1000
            hdist.append(dist)
            
        for element in rating:
            hrating.append(float(element.text))
            
        for element in price:
            p = element.text
            hprice.append(int(p.split()[1].replace(',','')))
            
        for element in comments:
            comment = element.text
            if comment == 'Review score ':
                    comment = 'Rating under 7'
            hcomments.append(comment)
            

    i = 1
    while i < maxpagenum:
        i = i+1

        nextapgexpath ='//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[4]/div[2]/nav/nav/div/div[3]/button'

        nextapge_button = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, nextapgexpath)))

        nextapge_button.click()
        time.sleep(2)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        properties = soup.find_all('div', {'class': 'c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4', 'data-testid':'property-card'})
        for k, property in enumerate(properties):
            names = property.find('div', {'class':'f6431b446c a15b38c233', 'data-testid':'title'})
            locations = property.find('span', {'class':'aee5343fdb def9bc142a', 'data-testid':'address'})
            distances = property.find('span',{'data-testid':"distance"})
            rating = property.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
            price = property.find('span', {'class': 'f6431b446c fbfd7c1165 e84eb96b1f', 'data-testid':"price-and-discounted-price"})
            comments = property.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
            if names == None:
                names = []
                
                hnames.append(np.nan)
            if locations == None:
                locations = []
                
                hlocations.append(np.nan)
            if distances == None:
                distances = []
                
                hdist.append(np.nan)
            if rating == None:
                rating = []
                
                hrating.append(np.nan)
            if price == None:
                price = []
                
                hprice.append(np.nan)
            if comments == None:
                comments = []
                
                hcomments.append(np.nan)

            for element in names:
                hnames.append(element.text)
                
            for element in locations:
                hlocations.append(element.text)
                
            for element in distances:
                dist = float(element.text.split(' ')[0])
                if dist>99.9:
                    dist = dist/1000
                hdist.append(dist)
                
            for element in rating:
                hrating.append(float(element.text))
                
            for element in price:
                p = element.text
                hprice.append(int(p.split()[1].replace(',','')))
                
            for element in comments:
                comment = element.text
                if comment == 'Review score ':
                        comment = 'Rating under 7'
                hcomments.append(comment)
                

    driver.quit()
    data = pd.DataFrame({'name':hnames,'location':hlocations,'price':hprice,'ratings':hrating,'distance':hdist,'comments':hcomments})
    data.to_csv(f'Hotel_{location}_{checkin}_{checkout}.csv')
    return data

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python webcrawler.py <location> <checkin_date> <checkout_date>")
        sys.exit(1)

    location = sys.argv[1]
    checkin_date = sys.argv[2]
    checkout_date = sys.argv[3]

    webcrawler(location, checkin_date, checkout_date)