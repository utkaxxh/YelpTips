# selenium packages
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# All exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import errno

########################################################################################################################################## 
########################################################################################################################################## 


# extraction and scrapping packages
from bs4 import BeautifulSoup
import os
import re

def init_driver():    
    #make browser
    ua=UserAgent()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (ua.random)
    service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
    # provide the path for the chrome driver
    driver = webdriver.Chrome('/Users/utkarsh/Desktop/Fall-2017-Cources/BIA-660A/WebAnalytics-BIA-660A-/week10/chromedriver',desired_capabilities=dcap,service_args=service_args)
    return(driver)

########################################################################################################################################## 


def login(driver,username,passwrd):
    #access website
    driver.get('https://www.yelp.com/')
    
    #find and click login icon
    icon=driver.find_element_by_xpath('//*[@id="header-log-in"]/a')
    icon.click()
    
    
    #find and fill the login credientials
    form = driver.find_element_by_id('ajax-login')
    try:
        myElem = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ajax-login"]/button')))
    except TimeoutException:
        print('Looking took much longer')
    email = form.find_element_by_id('email')
    # you can use your own mail id if you have
    email.send_keys(username)
    
    time.sleep(2)
    #find and fill the password box
    password = form.find_element_by_id('password')
    # own password
    password.send_keys(passwrd)

    
    #find and click the login button
    button=driver.find_element_by_xpath('//*[@id="ajax-login"]/button')
    time.sleep(2)
    button.click()
    time.sleep(2)

########################################################################################################################################## 

def ScrapRestro(query,location):
    # example Indian Restaurant in NewYork,NY
    try:
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header-search-submit"]')))
        
        search = driver.find_element_by_id("find_desc")
        search.send_keys(query)
        time.sleep(2)
        city = driver.find_element_by_id("dropperText_Mast")
        city.click()
         # Find the search box
        city.send_keys(Keys.DELETE + location)
        time.sleep(2)
        #find and click the search button
        searchBtn = driver.find_element_by_id("header-search-submit")
        time.sleep(2)
        searchBtn.click()
    except TimeoutException:
        print ("Loading took too much time!")
    
        
    outer_condition = 1
    while outer_condition == 1:
        
        html = driver.page_source 
        print(driver.current_url)
        main_url= driver.current_url
        time.sleep(1)
        soup = BeautifulSoup(html,'lxml')
        links = soup.find_all("h3",{"class":"search-result-title"}) #links to all the restro on a given page
        
        for link in links[1:]:
            res_name = ''.join(map(lambda x: x.strip(), link.strings)) # fetches all the restro names
            res_url = 'https://www.yelp.com/' + link.find('a').get('href') # create a URL's for the above fetched restro
            if not re.search('adredir',res_url): # the if condition is used to filter out all ads
                driver.get(res_url)
                time.sleep(1)
            file= open('/Users/utkarsh/Desktop/BIA_project/latestchinesedishes.txt','a')
            try:
                menu = driver.find_element_by_partial_link_text('View the full menu')
                menu.click()
                print(driver.current_url)
                time.sleep(3)
                html = driver.page_source
                soup = BeautifulSoup(html,'lxml')
                divs = soup.find_all("div",{"class":"arrange_unit arrange_unit--fill menu-item-details"}) #links to all the restro on a given page
                for div in divs: 
                    review_content = div.find('h4') 
                    menus = str(review_content.text).replace('\n','')
                    menus = menus.replace('  ','')
                    file.write(menus)
                    file.write('\n')
                    
                    
                print('menus added to set for restro: ',res_name)
                file.close()
            
            except(NoSuchElementException, StaleElementReferenceException) as e: 
                print('menu link not found')
          
        driver.get(main_url)
        time.sleep(3)
        try:
            continue_link = driver.find_element_by_partial_link_text('Next')
            continue_link.click()
            time.sleep(2)
        
        except (NoSuchElementException, StaleElementReferenceException) as e: 
            outer_condition = 0

########################################################################################################################################## 
           


if __name__ == "__main__":
    
    username = 'williamcannady1@outlook.com'
    password = 'Stevens@1234'
    driver = init_driver()
    query = input("what do you want to search? ")
    location = input("where do you want to find it ? ")
    login(driver,username,password)
    ScrapRestro(query,location)
    
