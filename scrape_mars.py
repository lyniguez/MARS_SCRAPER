# Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests
import tweepy
import json


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():
    browser = init_browser()
    listings = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'html.parser')

    listings["news_title"] = soup.find_all("div", class_="content_title")[0].text    
    listings["news_paragraph"] = news_paragraph = soup.find_all("div", class_="rollover_description_inner")[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')

    image = soup.find('a',class_="button fancybox")['data-fancybox-href']

    main = 'https://www.jpl.nasa.gov'

    image_url = main+image

    listings["image_url"] = image_url

    # twitter key/tokens
    consumer_key = "PrGevwVABchoG0o589r9BPTPM"
    consumer_secret = "wUJAaOLJdNgE2WIewNPYhhsqazrRCdSplJmwqqAm7Wh6pNejE8"
    access_token = "905540398994612227-t60QDxW0jHuOXAlPSTteYE1CyO6CMAZ"
    access_token_secret = "BdTYVNH6m2dUtkrFAf6PQyHuh22WD0U0r3onfivP7yjr7"


    # Setup Tweepy API Authentication

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Target User Account
    target_user = "@MarsWxReport"

    # Retrieve and print latest tweet
    mars_weather = api.user_timeline(target_user, count = 1)

    for tweet in mars_weather:
        mars_tweet = tweet["text"]

    listings["twitter"] = mars_tweet
    
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    
    df = tables[0]
    df.columns = ['','Values']

    spaceFactsDF = df.set_index('')
    spacefacts = spaceFactsDF.to_html(bold_rows=True)

    listings["mars_facts"] = spacefacts

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find all div classes 'item'
    hemispheres = soup.find_all('div', class_="item")

    # get list of URLs for each hemisphere
    img_url_text = []

    for item in hemispheres:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        
        link = item.find('a')
        href = link['href']
       
        #print('-----------')
        #print(header.text)
       
        url = ('https://astrogeology.usgs.gov' + href)
        #print(url)
        
        #dict = {'title':header.text}
        #titles.append(dict)
        img_url_text.append(url)
        
        
    # run for loop going through each url and getting the title and sample url
    # put values in as dictionary
    hemisphere_image_urls = []

    for url in img_url_text:
    
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        titles = soup.find('h2',class_="title")
    
        browser.click_link_by_text('Sample')
        
        img = browser.windows[0].next.url
        
        urls = {
            'title':titles.text,
            'img_url':img
        }
         
        hemisphere_image_urls.append(urls)

    listings["hemisphere"] = hemisphere_image_urls
    
    
    return listings

