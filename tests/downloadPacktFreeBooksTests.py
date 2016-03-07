#!/usr/bin/env python
import requests
import os
import sys
import configparser
import re
from collections import OrderedDict
from bs4 import BeautifulSoup


class MyPacktPublishingBooksDownloader(object):
    
    def __init__(self):
    
        #for codec in ['latin_1', 'utf_8', 'utf_16','ascii']:
        #    print(codec, 'Łószczykięwicz'.encode(codec,errors='ignore'), sep='\t')
        #    print('Łószcz')
        #sys.exit(1)
        self.packtPubUrl= "https://www.packtpub.com"
        self.myBooksUrl= "https://www.packtpub.com/account/my-ebooks"
        self.loginUrl= "https://www.packtpub.com/register"
        self.myPacktEmail, self.myPacktPassword= self.getLoginData("configFileMine.cfg")
        self.session= None
        self.bookData=None
        #self.createSession()
    
    def getLoginData(self, cfgFilePath):
        config =configparser.ConfigParser()
        try:
            if(not config.read(cfgFilePath)):
                raise configparser.Error('configFile.cfg file not found')
            email= config.get("LOGIN_DATA",'email')
            password= config.get("LOGIN_DATA",'password')
            return (email,password)
        except configparser.Error as e:
            print("[ERROR] configFile.cfg file incorrect or doesn't exist! : "+str(e))
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
            import codecs
            f = codecs.open('myebook.txt','r', encoding='utf-8',errors='ignore')
            file=f.read()
            myBooksHtml = BeautifulSoup(file,'html.parser')
            #print(myBooksHtml.original_encoding)
            all =  myBooksHtml.find(id='product-account-list').find_all('div', {'class':'product-line unseen'})
            self.bookData= [ {'title': attr['title'].replace('[eBook]','').rstrip(' '), 'id':attr['nid']}   for attr in all]
            #print(bookData)
            for i,div in  enumerate(myBooksHtml.find_all('div', {'class':'product-buttons-line toggle'})):
                downloadUrls= {}
                for a_href in div.find_all('a'):
                    m = re.match(r'^(/[a-zA-Z]+_download/(\w+)(/(\w+))*)',a_href.get('href'))
                    if m:
                        if m.group(4) is not None:
                           downloadUrls[m.group(4)]= m.group(0)
                        else:
                            downloadUrls['code']= m.group(0)
                        #print(m.group(4))
                        pass
                #print(downloadUrls)
                self.bookData[i]['downloadUrls']=downloadUrls
            print(self.bookData )        
        except requests.exceptions.RequestException as exception:
            print("[ERROR] - Exception occured %s "%exception )

     
if __name__ == '__main__':
    
    downloader = MyPacktPublishingBooksDownloader()
    downloader.getDataOfAllMyBooks()
    input("Press a button to exit...")