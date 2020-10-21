#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'

    browser.visit(news_url)

    html = browser.html

    news_soup = BeautifulSoup(html, 'html.parser')

    news_title = news_soup.find_all('div', class_='content_title')[1].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    print(news_title)
    print("--------------------------------------------------------------------")
    print(news_p)

    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(images_url)

    html = browser.html

    images_soup = BeautifulSoup(html, 'html.parser')

    relative_image_path = images_soup.find('article')['style']

    featured_image_url = jpl_nasa_url + relative_image_path
    print(featured_image_url)

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    tables = pd.read_html(url)

    df = tables[0]
    df

    html_table = df.to_html()
    html_table

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres , 'html.parser')

    # Retreive all items 
    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'


    # Loop through the items previously stored
    for item in items: 
    # Store title
        title = item.find('h3').text
    
    # Store link that leads to full image website
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
    
    # Visit website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
    # Parse each website's HTML
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
    # Retrieve source of full image 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data

