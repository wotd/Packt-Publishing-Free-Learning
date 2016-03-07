#!/usr/bin/env python

__author__ = "Lukasz Uszko"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "lukasz.uszko@gmail.com"

import requests
import os
import sys
import configparser
import re
from collections import OrderedDict
from bs4 import BeautifulSoup


class MyPacktPublishingBooksDownloader(object):
    
    def __init__(self,session=None):
    
        #for codec in ['latin_1', 'utf_8', 'utf_16','ascii']:
        #    print(codec, 'Łószczykięwicz'.encode(codec,errors='ignore'), sep='\t')
        #    print('Łószcz')
        #sys.exit(1)
        self.packtPubUrl= "https://www.packtpub.com"
        self.myBooksUrl= "https://www.packtpub.com/account/my-ebooks"
        self.loginUrl= "https://www.packtpub.com/register"
        self.myPacktEmail, self.myPacktPassword,self.downloadFolderPath= self.getLoginData("loginDataMine.cfg")
        self.session= session
        if self.session is None:
            self.createSession()
        self.bookData=None
        
    
    def getLoginData(self, cfgFilePath):
        config =configparser.ConfigParser()
        try:
            if(not config.read(cfgFilePath)):
                raise configparser.Error('loginData.cfg file not found')
            email= config.get("LOGIN_DATA",'email')
            password= config.get("LOGIN_DATA",'password')
            downloadPath= config.get("LOGIN_DATA",'downloadFolderPath')
            return (email,password,downloadPath)
        except configparser.Error as e:
            print("[ERROR] loginData.cfg file incorrect or doesn't exist! : "+str(e))
            sys.exit(1)
    
    def createSession(self):
        reqHeaders= {'Content-Type':'application/x-www-form-urlencoded',
                    'Connection':'keep-alive'}
        formData= {'email':self.myPacktEmail,
                'password':self.myPacktPassword,
                'op':'Login',
                'form_build_id':'',
                'form_id':'packt_user_login_form'}
        try:
            #to get form_build_id
            print("Creates session ...")
            r = requests.get(self.loginUrl,timeout=10)
            content = BeautifulSoup(str(r.content), 'html.parser')
            formBuildId = [element['value'] for element in content.find(id='packt-user-login-form').find_all('input',{'name':'form_build_id'})]
            #print(formBuildId[0] )
            formData['form_build_id']=formBuildId[0]
        except requests.exceptions.RequestException as exception:
            print("[ERROR] - Exception occured %s "%exception )
                
        try:
            self.session = requests.Session()
            rPost = self.session.post(self.loginUrl, headers=reqHeaders,data=formData)
            if(rPost.status_code is not 200):
                raise requests.exceptions.RequestException("login failed! ")               
        except requests.exceptions.RequestException as exception:
            print("[ERROR] - Exception occured %s "%exception )
            sys.exit(1)
            
    def getDataOfAllMyBooks(self):
        try:
            print("Getting books data ...")
            r = self.session.get(self.myBooksUrl,timeout=10)
            if(r.status_code is 200):
                print("opened  '"+ self.myBooksUrl+"' succesfully!")
            myBooksHtml = BeautifulSoup(r.text, 'html.parser')
            all =  myBooksHtml.find(id='product-account-list').find_all('div', {'class':'product-line unseen'})
            self.bookData= [ {'title': attr['title'].replace('[eBook]','').rstrip(' '), 'id':attr['nid']}   for attr in all]
            #print(bookData)
            for i,div in enumerate(myBooksHtml.find_all('div', {'class':'product-buttons-line toggle'})):
                downloadUrls= {}
                for a_href in div.find_all('a'):
                    m = re.match(r'^(/[a-zA-Z]+_download/(\w+)(/(\w+))*)',a_href.get('href'))
                    if m:
                        if m.group(4) is not None:
                           downloadUrls[m.group(4)]= m.group(0)
                        else:
                            downloadUrls['code']= m.group(0)
                self.bookData[i]['downloadUrls']=downloadUrls
            #print(self.bookData)      
        except requests.exceptions.RequestException as exception:
            print("[ERROR] - Exception occured %s "%exception )
            
            
    def downloadBooks(self,titles=None,formats=None): #titles= ['C# tutorial', 'c++ Tutorial'] ; format=('pdf','mobi','epub','code')
        try:
            #download a book
            if formats is None:
                formats=('pdf','mobi','epub','code')              
            if titles is not None:
                tempBookData = [data for i,data in enumerate(self.bookData) if any(data['title']==title for title in titles) ]
                #print(tempBookData )
            else:
                tempBookData=self.bookData
            nrOfBooksDownloaded=0
            for i, book in enumerate(tempBookData):
                for format in formats:
                    print(format)
                    if format in tempBookData[i]['downloadUrls'].keys():
                        if format == 'code':
                            print("downloading code for eBook: '"+tempBookData[i]['title']+ "'...")                           
                        else:
                            print("downloading eBook: '"+tempBookData[i]['title']+"' in '."+format+ "' format...")
                        r = self.session.get(self.packtPubUrl+tempBookData[i]['downloadUrls'][format],timeout=100)
                        if(r.status_code is 200):
                            if format == 'code':
                                format='zip'
                            with open(''.join(list(map(str.capitalize, tempBookData[i]['title'].split(' '))))+'.'+format,'wb') as f:
                                f.write(r.content)
                            if format == 'code':
                                print("[SUCCESS] code for eBook: '"+tempBookData[i]['title']+"' downloaded succesfully!")                           
                            else:
                                print("[SUCCESS] eBook: '"+tempBookData[i]['title']+'.'+format+"' downloaded succesfully!")      
                            nrOfBooksDownloaded=i+1
                        else:
                            raise requests.exceptions.RequestException("Cannot download "+tempBookData[i]['title'])                            
            print(str(nrOfBooksDownloaded)+" eBooks have been downloaded !")          
        except requests.exceptions.RequestException as exception:
            print("[ERROR] - Exception occured during GET request%s "%exception )
        except IOError as exception:
            print("[ERROR] - Exception occured durin opening file %s "%exception )
        
       
        
if __name__ == '__main__':
    
    downloader = MyPacktPublishingBooksDownloader()
    downloader.getDataOfAllMyBooks()
    downloader.downloadBooks(titles=['Unity 4.x Game AI Programming'], formats=("pdf",))
    print("--done--")