#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from webbot import Browser

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

import time


class kPage():
    URL = 'https://www.k-online.de/vis/v1/de/search?oid=102636&lang=1&_query=&'\
        'f_type=profile&f_country=IT&_sort=alpha_asc'
    CLASS_NAME = 'searchresult-item'
    SCROLL_PAUSE_TIME = 1.
    #TAG = 'media__body searchresult-box__media__body one-whole'
    
    
    def __init__(self, ShowBrowser=True):
        """
        Login into the CAMed cloud located at the Medical University Graz, and 
        created for the COMET projroct CAMed. The cloud alos has a filing system
        to store and transport results and other data.

        Parameters
        ----------
        ShowBrowser : Boolean, optional
            Show browser window. The default is True.

        Returns
        -------
        None.

        """
        options=ChromeOptions()
        if not ShowBrowser:
            options.add_argument('headless')
            options.add_argument('window-size=1200x600')
        
        self.__browser = Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        self.__browser.get(self.URL)
       
    
    def closeCookies(self):
        name = 'Save Settings'
        id = '#usercentrics-root'

        item = self.__browser.execute_script("return document.querySelector("\
             "'{}').shadowRoot".format(id))

        for b in item.find_elements(By.TAG_NAME, 'button'): 
            if b.text.startswith(name):
                b.click()
                return True
            
    
    def scrollToButtom(self):
        driver = self.__browser
        last_height = driver.execute_script("return document.body.scrollHeight")
        i=0
        while True and i < 5:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(self.SCROLL_PAUSE_TIME)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height==last_height:
                break
            else:
                last_height=new_height  
        pass
        
    
    def getEntries(self):
        srList = self.__browser.find_elements(By.CLASS_NAME, self.CLASS_NAME)
        name=[]
        location=[]
        tags=[]
        for i, sr in enumerate(srList):
            name.append(sr.find_element(By.TAG_NAME, 'h3').text)
            location.append(sr.find_element(By.TAG_NAME, 'h5').text)
            'html body div#site-wrapper.vis-page-wrapper.page-wrapper div.inner-wrap.inner-wrap--padding div.page.page--padding.search.push--top div.search__item--results div#vis-search-scroll-area div.searchresult-list div.searchresult-item.searchresult-item--premium div.list-tag-labels.flex.flex--align-end div.flex__item.flex__item--grow'
            try:
                tags.append(sr.find_element(By.CLASS_NAME,
                    'flex__item--grow').find_element(By.TAG_NAME, 'span').text)
            except:
                tags.append('')
        #print(name, location, tags)
        return name, location, tags
            
    
    def makeList(self, name, location, tags, path):
        fn = '/ItalyProvince.dat'
        prov={}
        with open(path+fn, 'r') as f:
            for line in f.readlines():
                id, p = line.replace(' ', '').split('\t')[3:5]
                prov.update({id:p})
        
        with open(path+'/companies.csv', 'w') as f:
            f.write('\Company,location,province,tag')
            for n, loc, tag in zip(name, location, tags):
                line = n+','
                l = loc.split('(')
                if len(l) != 1:
                    line+=l[0].replace(' ', '')+','
                    ID=l[-1].replace(')', '')+','
                    for key, item in prov.items():
                        if ID.startswith(key):
                            line+=item
                else:
                    line+=l[0].replace(' ', '')+',,'
                    
                line+=tag
                f.write('\n'+line)
        pass
    
    
    def close(self):
        self.__browser.quit()
        

if __name__=='__main__':
    kp=kPage(ShowBrowser=False)
    time.sleep(1.5)
    kp.closeCookies()
    kp.scrollToButtom()
    
    name, location, tags = kp.getEntries()
    kp.makeList(name, location, tags, os.path.dirname(os.path.abspath(__file__)))
    
    kp.close()