#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:03:17 2017

@author: deepanshparab
"""
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



# extraction and scrapping packages
from bs4 import BeautifulSoup
import os
import re


########################################################################################################################################## 
########################################################################################################################################## 
def init_driver():    
    #make browser
    ua=UserAgent()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (ua.random)
    service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
    # provide the path for the chrome driver
    driver = webdriver.Chrome('/Users/deepanshparab/Desktop/Fall-2017-Cources/BIA-660A/WebAnalytics-BIA-660A-/week10/chromedriver',desired_capabilities=dcap,service_args=service_args)
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
    #indian restro in nyc
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
    

#    While condition is used to check if a given webpage has <Next> icon to go from one web page to other..
#    This is the outer while loop which runs through various restro in NYC....till have <Next> icon 

    outer_condition = 1
    outer_loop = 0
    while outer_condition == 1:
        
        html = driver.page_source 
        print(driver.current_url)
        main_url= driver.current_url
        time.sleep(1)
        soup = BeautifulSoup(html,'lxml')
        links = soup.find_all("h3",{"class":"search-result-title"}) #links to all the restro on a given page
        for link in links[1:]:
            res_name = ''.join(map(lambda x: x.strip(), link.strings)) # fetches all the restro names
            dir_name = MkResDir(res_name) # creating directory
            res_url = 'https://www.yelp.com/' + link.find('a').get('href') # create a URL's for the above fetched restro
            if not re.search('adredir',res_url): # the if condition is used to filter out all ads
                driver.get(res_url)
                time.sleep(1)
                
                inner_condition = 1
                inner_loop = 0
                while inner_condition == 1:
                     try:
                        continue_link = driver.find_element_by_partial_link_text('Next')
                        continue_link.click()
                        time.sleep(3)
                        page = driver.page_source
                        # code for putting the data into the file    
                        inner_loop = inner_loop +1
                        WriteFiles(dir_name,page,inner_loop)
                        print('Review '+str(inner_loop)+' Created')
                     
                     except(NoSuchElementException, StaleElementReferenceException) as e: 
                         inner_condition = 0
                     
                     print(driver.current_url)
                     print(inner_loop)
                
                
                print('done with restro %r'%(res_name))
            
            
        driver.get(main_url)
        time.sleep(3)
        try:
            continue_link = driver.find_element_by_partial_link_text('Next')
            continue_link.click()
            time.sleep(2)
            outer_loop = outer_loop +1
        
        except (NoSuchElementException, StaleElementReferenceException) as e: 
            outer_condition = 0
            
        print(outer_loop)
        
##########################################################################################################################################            

def MkResDir(resname):
    base_path = '/Users/deepanshparab/Desktop/Fall-2017-Cources/BIA-660A/WebAnalytics-BIA-660A-/Project/Data'
    filename = base_path+'/Chinese/'+resname
    
    if not os.path.exists((filename)):
        try:
            os.makedirs(filename)
            
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                print('dir not found')
    return filename
########################################################################################################################################## 

def WriteFiles(filename,page,number):
    reviewfile = str(filename+'/'+'reviewpage_'+str(number))+'.txt'
    if not os.path.exists(reviewfile):
        try:
            file = open(reviewfile,'w')
            file.write(page)
            file.close()
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                print('dir not found')
    
########################################################################################################################################## 
##########################################################################################################################################    

if __name__ == "__main__":
    
    username = 'scomp9923@gmail.com'
    password = 'scomp@123'
    driver = init_driver()
    
    query = input("what do you want to search? ")
    location = input(" where do you want to find it? ")
    login(driver,username,password)
    ScrapRestro(query,location)
    base_path = '/Users/deepanshparab/Desktop/Fall-2017-Cources/BIA-660A/WebAnalytics-BIA-660A-/Project/Data'
    time.sleep(5)
    driver.quit()

    
'''
login password:
jjepins@123,jjepins@gmail.com,jjepins@123
webproj1@outlook.com,hoboken1
williamcannady1@outlook.com,Stevens@1234
keranshah95@mail.com,Keranshah@95
'''


   

