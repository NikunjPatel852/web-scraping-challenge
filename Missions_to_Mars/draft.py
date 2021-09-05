from sys import executable
import pandas as pd 
from bs4 import BeautifulSoup as bs 
from splinter import Browser, browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium import webdriver
import time

def init_browser(): 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless= False)

mars_web = {}
hemisphere_image_urls = []

def scrape_news():
    browser = init_browser()
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html 
    news_soup = bs(html, "html.parser")
    articles = news_soup.find_all('div', class_='col-md-8')

    for articles in articles: 
        news_date = articles.find('div',class_='list_date').text
        news_title = articles.find('div', class_='content_title').text
        news_par = articles.find('div', class_='article_teaser_body').text 
        break
    
    mars_web['news_date'] = news_date
    mars_web['news_title'] = news_title
    mars_web['news_par'] = news_par

    browser.quit()
    return mars_web

def scrape_image():
    browser = init_browser()
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    html = browser.html 
    soup2 = bs(html,'html.parser')
    full_image = soup2.find_all('a', class_='fancybox-thumbs')

    for pic in full_image:
        featured_image_url=f"https://spaceimages-mars.com/{pic['href']}"
        print(featured_image_url)
        break
    
    mars_web['featured_image_url'] = featured_image_url

    browser.quit()
    return mars_web

def scrape_facts():
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["ID", "Properties", "Mars", "Earth"]
    mars_web['mars_facts'] = mars_facts 

    browser.quit()
    return mars_web

def scrape_astro():

    browser = init_browser()
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')

    items = soup.find_all('div', class_='item')
    hemispheres_main_url = 'https://marshemispheres.com/'
    for item in items: 
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + image_url)
        image_html = browser.html
        soup = bs( image_html, 'html.parser')
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

    print(f"Hemisphere Image URLs")
    print()
    print("-------------------------------------------------")
    print()
    print(f"Cerberus Hemisphere Enhanced:\n{hemisphere_image_urls[0]}")
    print()
    print(f"Schiaparelli Hemisphere Enhanced:\n{hemisphere_image_urls[1]}")
    print()
    print(f"Syrtis Major Hemisphere Enhanced:\n{hemisphere_image_urls[2]}")
    print()
    print(f"Valles Marineris Hemisphere Enhanced:\n{hemisphere_image_urls[3]}")

    browser.quit()
    return mars_web
    