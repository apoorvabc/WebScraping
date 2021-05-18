from pathlib import Path
import csv

from selenium import webdriver
from bs4 import BeautifulSoup
import time

DRIVER_PATH = str(Path('geckodriver.exe').resolve())
path = "D:/Documents/Digital Engineering OVGU/Scrape JS_website/chromedriver.exe"
browser = webdriver.Chrome(path)
browser.get('https://www.amazon.com/s?k=canon+5d&page=1&qid=1621180750&ref=sr_pg_2')
    

def write_csv(ads):
    with open('results.csv', 'a') as f:
        fields = ['title', 'url', 'price']

        writer = csv.DictWriter(f, fieldnames=fields)

        for ad in ads:
            writer.writerow(ad)



def get_html(url):
    time.sleep(3)
    # browser = webdriver.Firefox(executable_path=DRIVER_PATH)
    return  browser.page_source

def scraped_data(card):
    try:
        h2 = card.h2
    except:
        title = ''
        url = ''
    else:
        title = h2.text.strip()
        url = h2.a.get('href')
    try:
        price = card.find('span', class_ = 'a-price-whole').text.strip('.').strip()
    except:
        price = ''
    else:
        price = ''.join(price.split(','))
        print(price)
        
    data = {'title': title, 'url':url, 'price' : price}
    return data


def main():
    ads_data = []
    for i in range (1,4):
        url= f'https://www.amazon.com/s?k=canon+5d&page={i}&qid=1621180750&ref=sr_pg_2'
        html = get_html(url)
        soup =  BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div',{'data-asin': True, 'data-component-type' : 's-search-result'})
        print(len(cards))
        
        
        for card in cards:
            data = scraped_data(card)
            ads_data.append(data)
 
    write_csv(ads_data)
    
if __name__ == '__main__':
    main()