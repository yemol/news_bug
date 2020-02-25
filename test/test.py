from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

def getOneNews_A9VG(articleUrl):
    html = urlopen('http://www.a9vg.com' + articleUrl)
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
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

def getExternalLink(bs,excludeUrl):
    externalLinks = []
    for link in bs.findAll('a',href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks
    

urlStr = "http://www.a9vg.com/list/news"
html = urlopen(urlStr)
bs = BeautifulSoup(html,'html.parser')
# for link in bs.find('ul',{'class':re.compile('^vd-flexbox vdp-direction_column(.)*$')}).findAll('a'):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])
#         # text = link.find('div',{'class':re.compile('^vd-flexbox a9-rich-card-list_label(.)*$')}).text
#         # print(text)
#         # time = link.find('div',{'class':'vd-flexbox vdp-gap_small'}).text
#         # print(time)
#         print(getOneNews_A9VG(link.attrs['href']))
#         print("--"*20)

domain = '{}://{}'.format(urlparse(urlStr).scheme,urlparse(urlStr).netloc)
print (domain)
internal = getInternalLink(bs,domain)
for link in internal:
    print(link)
    
print("++"*20)

external = getExternalLink(bs,urlparse(urlStr).netloc)
for link in external:
    print(link)
        