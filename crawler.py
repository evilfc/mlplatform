#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
from scrapy.selector import Selector

"""
实现新浪微博爬虫，需要模拟登录。
使用到两个模块：
requests：用于HTTP请求和回复
scrapy：爬虫模块，使用了其中的选择器
"""

"""
第一步：访问http://weibo.cn/pub/"得到最初始的cookie值
"""
s1_url = "http://weibo.cn/pub/"
s1_header = {
        "Accept":"text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*, q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN, zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"weibo.cn",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36) (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Safari/537.36"
}
s1_data = {"vt":"4"}
r = requests.get(s1_url, headers=s1_header, data=s1_data)
#print r.headers
s1_cookie = r.cookies['_T_WM']
