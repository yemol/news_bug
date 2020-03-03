from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import re

def getOneNews_A9VG(articleUrl):
    ua_header = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    html = urlopen('http://www.a9vg.com' + articleUrl,ua_header)
    bs = BeautifulSoup(html,'html.parser')
    
    article = bs.find('article')
    title = article.find('div',{'class':re.compile('^(.)*c-article-main_content-title(.)*$')}).text
    print(title)
    content = article.find('div',{'class':re.compile('^(.)*c-article-main_contentraw(.)*$')})
    print(content)
    return {'title':title,
            'content':content
            }

def getInternalLink(bs,includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,urlparse(includeUrl).netloc)
    internalLinks = []
    for link in bs.findAll('a',href=re.compile('^(/|.*' + includeUrl + ')')):
         if link.attrs['href'] is not None:                 #有href属性
             if link.attrs['href'] not in internalLinks:    #未被处理
                if link.attrs['href'].startswith('/'):     #内部链接
                    internalLinks.append({
                    'link':includeUrl + link.attrs['href'],
                    'text':link.text
                    })
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

def getExternalLink(bs,excludeUrl):
    externalLinks = []
    for link in bs.findAll('a',href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append({
                    'link':link.attrs['href'],
                    'text':link.text
                    })
    return externalLinks

def getPagelinks(urlStr):
    request = urllib.request.Request(urlStr)
    """添加浏览器特有头信息来保证不会被发觉为爬虫"""
    request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36")
    html = urlopen(request)
    bs = BeautifulSoup(html,'html.parser') 
    domain = '{}://{}'.format(urlparse(urlStr).scheme,urlparse(urlStr).netloc)
    print (domain)
    internal = getInternalLink(bs,domain)
    for link in internal:
        print(link)
        
    print("++"*20)
    
    external = getExternalLink(bs,urlparse(urlStr).netloc)
    for link in external:
        print(link)   


getPagelinks("http://www.a9vg.com/list/news")
print("---"*20)
getPagelinks("https://www.vgtime.com/topic/index.jhtml")
print("---"*20)
getPagelinks("https://www.gcores.com/news")


# for link in bs.find('ul',{'class':re.compile('^vd-flexbox vdp-direction_column(.)*$')}).findAll('a'):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])
#         # text = link.find('div',{'class':re.compile('^vd-flexbox a9-rich-card-list_label(.)*$')}).text
#         # print(text)
#         # time = link.find('div',{'class':'vd-flexbox vdp-gap_small'}).text
#         # print(time)
#         print(getOneNews_A9VG(link.attrs['href']))
#         print("--"*20)


        