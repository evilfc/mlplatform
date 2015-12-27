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

"""
第二步：得到登录页面，该页面中包含了隐藏属性，在请求header中要用到
"""
s2_url = "http://login.weibo.cn/login/"
s2_header = {
        "Accept":"text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*, q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN, zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"login.weibo.cn",
        "Referer":"http://weibo.cn/pub/?vt=4",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36) (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Safari/537.36"
}
#请求header中使用了第一次得到的cookie值
s2_header["Cookie"] = "_T_WM=%s" % s1_cookie
#backTitle无法解析，是中文字符，应该是“微博”之类的字符
s2_data = {
        "ns":"1",
        "revalid":"2",
        "backURL":"http://weibo.cn/",
        "backTitle":"%CE%A2%B2%A9",
        "vt":""
}
r = requests.get(s2_url, headers=s2_header)
#print r.headers
content = r.content
rnd_n = Selector(text=content).xpath('//div/form[@action]').extract()
pwd = Selector(text=content).xpath('//div/form/div/input[@type="password"]').extract()
vkey = Selector(text=content).xpath('//div/form/div/input[@name="vk"]').extract()
m = re.search('rand=\d+', rnd_n[0])
if m:
    rnd_n = m.group(0)
m = re.search('password_\d+', pwd[0])
if m:
    pwd = m.group(0)
m = re.search('\d+_\w+_\d+', vkey[0])
if m:
    vkey = m.group(0)
#print rnd_n
#print pwd
#print vkey
