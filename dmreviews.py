import time
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

"""
Funtion uses Selenium webdriver (Chrome) package to scrape the website
Input: URL of the given  website is given as an input argument
Returns: Page source of the web browser.

"""

def get_html(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless =  True
    path = "./chromedriver.exe"
    browser = webdriver.Chrome(path, options=chrome_options)
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 
    return  browser.page_source

"""
Funtion executes the fetching operation using the tags and class values obtained from the get_data
Input : The div, span and the class values obtained from the get_data class are given as input arguments.
Returns : Returns the review data obtained after scraping using Beautifulsoup

"""

def get_vals(titles, tag, cls):
    data = []
    j=1
    if(cls=='bv-off-screen'):
        ulList = titles.find_all(tag, class_ = cls)
        for li in ulList:
            text = li.text.split()
            try:
                if(text[1]=='von' and j!=1):
                    data.append(text[0])
            except:
                continue
            finally:
                j=j+1
        return data
    else:
        ulList = titles.find_all(tag, class_ = cls)
        for li in ulList:
            data.append(li.text)
        return data

"""
Funtion uses BeautifulSoup package to scrape through the html and also takes the input parameters for the get_vals function to fetch the rating, author, header and the review of the product
Input : URL of the given website as an input argument.
Returns : Returns the page count, number of reviews for the product along with the dataframe(contains the review details).

"""
def get_data(url):
    html = get_html(url)
    soup =  BeautifulSoup(html, 'lxml')
    my_text = {}
    title = soup.find('div',{'id':'app'})
    
    for titles in title:
        rating = get_vals(titles, 'span', 'bv-off-screen')
        author = get_vals(titles, 'span', 'bv-author')
        header = get_vals(titles, 'div', 'bv-content-title-container')
        review = get_vals(titles, 'div', 'bv-content-summary-body-text')
    
        my_text = {'5 Star Rating': rating, 'Author name': author, 'Review Header': header, 'Review' :review}
        df = pd.DataFrame(my_text)
        
    #get page number
    page = soup.find('div', class_ = 'bv-content-pagination').get_text()
    rev_cnt = page.split()[0].split("-")[1]
    rev_cnt_end = page.split()[2]
    return rev_cnt,rev_cnt_end,df

"""
Main Function which contains the URL where the data scraped is appended and the CSV file is created.
Output : A csv file which contains reviews of the given product in the website

"""

def main():
    i=1
    my_df = pd.DataFrame(columns=['5 Star Rating','Author name','Review Header','Review'])
    while(True):
        url = f'https://www.dm.de/glade-duftkerze-mit-glas-petals-und-blossom-p5000204193725.html?bvstate=pg:{i}/ct:r'
        rev_cnt,rev_cnt_end,df = get_data(url)
        my_df = my_df.append(df,ignore_index=True)
        if(int(rev_cnt)==int(rev_cnt_end)):
            break
        i+=1
    print(my_df)
    my_df.to_csv("./Reviews.csv", sep=',',index=False)


if __name__ == '__main__':
    main()

