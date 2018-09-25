
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
from datetime import date


# In[5]:



def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[82]:


# latest news clipping
def latest_news():
    browser = init_browser()
    latest_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(latest_news_url)
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")
    news_headline = soup.find_all("div", class_="article_teaser_body")
    clipping = news_headline[0].text
    title = soup.find_all("div", class_="content_title")
    clipping_title = title[0].a.text
    browser.quit()
    return clipping_title, clipping
# works, good to go


# In[83]:


#latest featured image of mars
def featured_img():
    browser = init_browser()
    featured_img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_img_url)
    browser.click_link_by_id('full_image')
    browser.is_element_present_by_text('more info', wait_time=1)
    browser.click_link_by_partial_text('more info')
    html_info = browser.html
    soup = BeautifulSoup(html_info, "html.parser")
    image = soup.find("figure", class_="lede")
    img_info = image.a["href"]
    return f"https://www.jpl.nasa.gov{img_info}"


# In[ ]:


# mars weather
def mars_weather():
    browser = init_browser()
    mars_weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    html_weather = browser.html
    soup = BeautifulSoup(html_weather,"html.parser")
    tweet = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    tweet_info = tweet.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    browser.quit()
    return tweet_info
# good and works


# In[ ]:


#table mars data
def mars_facts():
    mars_facts_url = "https://space-facts.com/mars/"
    page = requests.get(mars_facts_url, headers=headers).text
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find_all("table", {"id":"tablepress-mars"})
    new_table = table[0]
    return new_table
# works as table grab


# In[74]:


#images for mars hemispheres
def hemi_info():
    browser = init_browser()
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    hemi_images = []
    items = browser.find_by_css('.item h3')
    for item in range(len(items)):
        hem_dict = {}
        browser.find_by_css('.item h3')[item].click()
        hemi1 = browser.find_link_by_text('Sample')
        hem_dict["link"] = hemi1["href"]
        hem_dict["title"] = browser.find_by_css("h2.title").text
        hemi_images.append(hem_dict)
        browser.back()
    browser.quit()
    return hemi_images

def scrape_all():

    clipping_title, clipping = latest_news()

    data = {
        "news_title": clipping_title,
        "news_paragraph": clipping,
        "featured_image": featured_img(),
        "hemispheres": hemi_info(),
        "weather": mars_weather(),
        "facts": mars_facts()
    }
    return data

# In[ ]:




