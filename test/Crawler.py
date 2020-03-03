# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from content import Website,Content

class Crawler:
    
    def getPage(self,url):
        try:
            ua_header = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}           
            req = requests.get(url,headers=ua_header)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text,'html.parser')
    
    def getContainer(self,bs,containerTag,containerClass):
        try:
            return bs.find(containerTag,attrs={'class':containerClass})
        except:
            return None
 
    
    def safeGet(self,pageObj,selector,getItem='text'):
        """用来取得内容的方法，如果没有找到，就返回空字符串"""
        selectedElem = pageObj.select(selector)
        if selectedElem is not None and len(selectedElem) > 0:
            return selectedElem[0]
        else:
            return None
    
   
    def parse(self,site):
        """从指定url提取内容"""
        
        bs =self.getPage(site.searchUrl)
        if bs is not None:
            bs = self.getContainer(bs,site.containerTag,site.containerClass)
            lists = bs.find_all(site.itemTag,attrs={'class':site.itemClass})
            for oneItem in lists:
                cover = self.safeGet(oneItem,site.elements['cover'])['src']
                title = self.safeGet(oneItem,site.elements['title']).text
                shortDesc = self.safeGet(oneItem,site.elements['shortDesc']).text
                dateTime = self.safeGet(oneItem,site.elements['dateTime']).text
                contennt = Content(site.name,site.url,cover,title,shortDesc,dateTime)
                contennt.print()                




                
crawler = Crawler()
siteData = [
    {
     'name':'A9VG',
     'url':'http://www.a9vg.com',
     'searchUrl':'http://www.a9vg.com/list/news',
     'container':'ul',
     'containerClass':'vd-flexbox vdp-direction_column vdp-align_stretch is-gap',
     'element':'li',
     'elementClass':'vd-flexbox a9-rich-card-list_item-gap',
     'itemList':{
         'cover':'img',
         'title':'.a9-rich-card-list_label',
         'shortDesc':'.a9-rich-card-list_summary',
         'dateTime':'.a9-rich-card-list_infos',
         }
    }
    # ['VGTime','https://www.vgtime.com/topic/index.jhtml','h1','div.StandardArticleBody_body_1gnLA'],
    # ['机核','https://www.gcores.com/news','h1','div.post-body']
    ]

websites = []
for row in siteData:
    oneSite = Website(row['name'],row['url'],row['searchUrl'],row['container'],row['containerClass'],row['element'],row['elementClass'])
    for key,item in row['itemList'].items():
        oneSite.addFetchElement(key,item)
    websites.append(oneSite)    


#print(websites[0].listFetchElement())
    

crawler.parse(websites[0])
        
