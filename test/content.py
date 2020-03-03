# -*- coding: utf-8 -*-

class Content:
    """所有文章/网页的共同基类"""
    
    def __init__(self,name,url,cover,title,short,created):
        self.name = name
        self.url = url
        self.cover = cover
        self.title = title
        self.short = short
        self.created = created
        
    def print(self):
        print("Name: {}".format(self.name))
        print("Url: {}".format(self.url))
        print("Cover: {}".format(self.cover))
        print("TITLE: {}".format(self.title))
        print("Short: {}\n".format(self.short))
        print("Created: {}\n".format(self.created))

    

class Website:
    """描述网站结构的信息"""
    
    def __init__(self,name,url,searchUrl,containerTag,containerClass,itemTag,itemClass):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.containerTag = containerTag
        self.containerClass = containerClass
        self.itemTag = itemTag
        self.itemClass = itemClass
        self.elements = {}
        
    def addFetchElement(self,name,selector):
        self.elements[name] = selector
        
    def listFetchElement(self):
        return self.elements