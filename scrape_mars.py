# Import Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)

    return browser 



# Define scrape and dictionary
def scrape():
    browser = init_browser()
    data_feed = {}
    output = marsNews(browser)
    data_feed["mars_news"] = output[0]
    data_feed["mars_text"] = output[1]
    data_feed["mars_link"] = output[2]
    data_feed["mars_image"] = marsImage(browser)
    data_feed["mars_weather"] = marsWeather(browser)
    data_feed["mars_facts"] = marsFacts(browser)
    data_feed["mars_hemisphere"] = marsHemi(browser)
    
    return data_feed
    

#  NASA Mars News

def marsNews(browser):
    url = 'https://mars.nasa.gov/news/'
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #browser = Browser("chrome", **executable_path, headless=True)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_listing = soup.find_all("div", class_='list_text')
    news_title = news_listing[0].find("div", class_='content_title').text
    news_link = news_listing[0].a['href']
    news_copy = news_listing[0].find('div', class_='article_teaser_body').text
    output = [news_title, news_copy, news_link]
    
    return output
 

# JPL Mars Space Images - Featured Images

def marsImage(browser):
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_image_button = browser.find_by_id("full_image")
    jpl_image_button.click()
    jpl_moreinfo_button = browser.links.find_by_partial_text("more info")
    jpl_moreinfo_button.click()
    html = browser.html
    soup_image = BeautifulSoup(html, "html.parser")
    jpl_result = soup_image.find("figure", class_='lede')
    jpl_image = jpl_result.a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + jpl_image
    
    return featured_image_url

# Mars Weather

def marsWeather(browser):
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    time.sleep(3)
    html = browser.html
    soup_tweet = BeautifulSoup(html, "html.parser")
    mars_tweet = soup_tweet.find("div", class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_tweet_text = mars_tweet.text
    mars_start = mars_tweet_text.find('InSight') + 8
    mars_end = mars_tweet_text.find('hPapic') - 1
    mars_weather=mars_tweet_text[mars_start:mars_end]
    
    return mars_weather


# Mars Facts

def marsFacts(browser):
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(mars_facts_url)
    mars_table = pd.DataFrame(mars_table[0])
    mars_facts = mars_table.to_html(header=False, index = False)
    
    return mars_facts
    
    
# Mars Hemispheres

def marsHemi(browser):
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    soup_hemis = BeautifulSoup(html, "html.parser")
    hemi_results = soup_hemis.find("div", class_='collapsible results')
    hemi_links = hemi_results.find_all("div", class_='item') 
    hemisphere_img_urls = []
    
    for link in hemi_links:
        title = link.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = link.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_img_urls.append({"title": title, "img_url": image_url})
    
    return hemisphere_img_urls
    
