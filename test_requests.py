# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup


ua_header = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
rq = requests.get("https://www.toutiao.com/c/user/6646873498/#mid=6646873498",headers=ua_header)

response = rq.text
bs = BeautifulSoup(response,'html.parser')
print(bs.body.a)
