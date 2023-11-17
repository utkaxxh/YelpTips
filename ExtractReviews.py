#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: utkarsh
"""
# all the pacakages required for the code
from bs4 import BeautifulSoup
import os
import sys


########################################################################################################################################## 
########################################################################################################################################## 
'''
In this function returns a dictionary which contains restro folder name as its key and the scrapped html pages as its values
eg : {'FishmarketRestaurant.txt': [reviewpage_1.txt,reviewpage_2.txt,reviewpage_3.txt,reviewpage_4.txt,reviewpage_5.txt,reviewpage_6.txt,reviewpage_7.txt,
reviewpage_8.txt,reviewpage_9.txt,reviewpage_12.txt,reviewpage_13.txt,reviewpage_14.txt,reviewpage_15.txt,reviewpage_16.txt,
reviewpage_17.txt,reviewpage_18.txt,reviewpage_19.txt]}
'''
def readRestaurant(inputdir):
    restro= {}
    for restroName in os.listdir(inputdir):
        if restroName =='.DS_Store':
            continue
        else:
            folder = os.path.join(inputdir,restroName)
            for reviews in os.listdir(folder):
                restro.setdefault(restroName,[]).append((str(os.path.join(folder,reviews))))
    return restro

########################################################################################################################################## 
########################################################################################################################################## 
'''
The function accepts input and output dir paths as parameters and creates a text files of the restro withs all the extracted reviews for that restro

'''
def extractRestaurant(inputpath,outputpath):
    restro = readRestaurant(inputpath)
    reviews_counter= 0
    for k,v in restro.items():
        #removing all the spaces if any in the file name
        k = k.replace(" ",'')
        filename = outputpath+'/'+str(k)+'.txt'
        try:
            restro_name = open(filename,'a')
        except IOError:
            print ("Could not read file:", filename)
            sys.exit()
        for files in v:
            try:
                html = open(files,'r')
            except IOError:
                print ("Could not read file:", files)
                sys.exit()
            soup = BeautifulSoup(html,'xml')
            
            reviews = soup.findAll('div', {'class':'review-content'})
            
            for review in reviews: 
                review_content = review.find('p',{'lang':'en'}) 
                data = review_content.text
                restro_name.write(data)
                restro_name.write('\n')
                reviews_counter = reviews_counter+1
                
        restro_name.close()
        print('Reviews successfully wrote in file '+k)
    print("total reviews extracted: "+str(reviews_counter))
    
             
if __name__ == "__main__":
    base_input_path = '/Users/utkarsh/Desktop/Project/Final_model/Data/Chinese'
    base_output_path ='/Users/utkarsh/Desktop/Project/Final_model/Data/test'
    extractRestaurant(base_input_path,base_output_path)

    
    
