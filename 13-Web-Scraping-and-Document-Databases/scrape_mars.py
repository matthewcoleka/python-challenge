from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


# Initialize browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

#Function to scrape for mars data
def scrape():
    #Initialize browser
    browser = init_browser()
   
    ### JPL Mars Space Images
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')
    feat_img = soup_jpl.find('footer').find('a')['data-fancybox-href'][31:40]
    feat_img_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/' + feat_img + 'hires.jpg'
     
    ### Mars Weather
    url_marsw = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_marsw)
    soup_marsw = BeautifulSoup(browser.html, 'html.parser')
    mars_weather = soup_marsw.find('div', class_='js-tweet-text-container').find('p').text
    
    ### Mars Facts
    ### Mars Facts
    url_marsfacts = 'http://space-facts.com/mars/'
    marsfacts = pd.read_html('http://space-facts.com/mars/')
    