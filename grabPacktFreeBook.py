#!/usr/bin/env python

__author__ = "Lukasz Uszko"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "lukasz.uszko@gmail.com"

import requests
import os
import sys
import configparser
from html.parser import HTMLParser
from bs4 import BeautifulSoup


if __name__ == '__main__':
    '''connection parameters'''
    config =configparser.ConfigParser()
    
    try:        
        if(not config.read("configFile.cfg")):
            raise configparser.Error('config file not found')       
        email= config.get("LOGIN_DATA",'email')
        password= config.get("LOGIN_DATA",'password')
        downloadBooksAfterClaim= config.get("DOWNLOAD_DATA",'downloadBookAfterClaim')
    except configparser.Error as e:
        print("[ERROR] loginData.cfg file incorrect or doesn't exist! : "+str(e))
        sys.exit(1)
        
    freeLearningUrl= "https://www.packtpub.com/packt/offers/free-learning"
    packtpubUrl= 'https://www.packtpub.com'
    reqHeaders= {'Content-Type':'application/x-www-form-urlencoded',
             'Connection':'keep-alive'}
    formData= {'email':email,
                'password':password,
                'op':'Login',
                'form_build_id':'',
                'form_id':'packt_user_login_form'}
    print("start grabbing eBook...")
    
    try:
        r = requests.get(freeLearningUrl,timeout=10)
        if(r.status_code is 200):
            html = BeautifulSoup(r.text, 'html.parser')
            loginBuildId= html.find(attrs={'name':'form_build_id'})['id']
            claimUrl= html.find(attrs={'class':'twelve-days-claim'})['href']
            bookTitle= html.find('div',{'class':'dotd-title'}).find('h2').next_element.replace('\t','').replace('\n','').strip(' ')
            if(loginBuildId is None or claimUrl is None or bookTitle is None ):
                print("[ERROR] - cannot get login data" ) 
                sys.exit(1)                
        else: 
            raise requests.exceptions.RequestException("http GET status codec != 200")
    except TypeError as typeError:
        print("[ERROR] - Type error occured %s "%typeError )
        sys.exit(1)
    except requests.exceptions.RequestException as exception:
        print("[ERROR] - Exception occured %s "%exception )
        sys.exit(1)

    formData['form_build_id']=loginBuildId
    session = requests.Session()
    
    try:
        rPost = session.post(freeLearningUrl, headers=reqHeaders,data=formData)
        if(rPost.status_code is not 200):
            raise requests.exceptions.RequestException("login failed! ")  
        print(packtpubUrl+claimUrl)
        r = session.get(packtpubUrl+claimUrl,timeout=10)
    except TypeError as typeError:
        print("[ERROR] - Type error occured %s "%typeError )
        sys.exit(1)
    except requests.exceptions.RequestException as exception:
        print("[ERROR] - Exception occured %s "%exception )
        sys.exit(1)
        
    if(r.status_code is 200):
        print("[SUCCESS] - eBook: '" + bookTitle +"' has been succesfully grabbed !")
        if downloadBooksAfterClaim=="YES":
            from packtFreeBookDownloader import MyPacktPublishingBooksDownloader
            downloader = MyPacktPublishingBooksDownloader(session)
            downloader.getDataOfAllMyBooks()
            downloader.downloadBooks([bookTitle], downloader.downloadFormats)            
    else:
        print("[ERROR] - eBook: '" + bookTitle +"' has not been grabbed, respCode: "+str(r.status_code))