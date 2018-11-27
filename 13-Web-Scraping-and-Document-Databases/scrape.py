from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#Function to scrape for
