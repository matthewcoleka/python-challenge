from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd


# Initialize browser
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#Function to scrape for mars data
def scrape():
    #Initialize browser
    browser = init_browser()

    ### NASA Mars News
    url_nasa_news = 'https://mars.nasa.gov/news/'
    html_nasa_news = requests.get(url_nasa_news)
    soup_nasa_news = BeautifulSoup(html_nasa_news.text, 'html.parser')
    #Collect the latest News Title and Paragraph Text
    news_title = soup_nasa_news.find('div', class_='content_title').text

    news_p= soup_nasa_news.find('div', class_='rollover_description_inner').text

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
    url_marsfacts = 'http://space-facts.com/mars/'
    marsfacts = pd.read_html('http://space-facts.com/mars/')
    marsfacts_df = marsfacts[0]
    marsfacts_df.columns = ['Category', 'Value']
    marsfacts_dict = marsfacts_df.to_dict('records')
    ### Mars Hemispheres
    url_marshemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    html_marshemi = requests.get(url_marshemi)
    soup_marshemi= BeautifulSoup(html_marshemi.text, 'html.parser')
    hemi = soup_marshemi.find_all('a', class_='itemLink product-item')
    hemisphere_url_list = []

    for link in hemi:
        hemi_dict = {}
        url_hemi = 'https://astrogeology.usgs.gov'+link['href']
        browser.visit(url_hemi)
        html_hemi = browser.html
        soup_hemi = BeautifulSoup(html_hemi, 'html.parser')
        image = soup_hemi.find('div', class_ = 'downloads').find('a')['href']
        title = soup_hemi.find('div', class_='content').find('h2').text
        hemi_dict = {
            "title": title,
            "img_url": image
        }
        hemisphere_url_list.append(hemi_dict)
    ### Store all scraped data in one python dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "jpl_featured_image":feat_img_url,
        "mars_weather": mars_weather,
        "mars_facts": marsfacts_dict,
        "mars_hemispheres": hemisphere_url_list

    }
    return mars_data
