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

"""
第三步：输入用户名和密码请求登录，这步使用的方法是POST方法。requests的POST方法data属性包含的是form_data，而请求时在URL中添加的参数不知道从哪里输入，所以这里将它们直接写在请求的URL中
"""
#上一步得到的随机数在请求的URL中会用到
s3_url = "http://login.weibo.cn/login/?" + rnd_n + "&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%E5%BE%AE%E5%8D%9A&vt=4&revalid=2&ns=1"
s3_header = {
        "Accept":"text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*, q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN, zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"login.weibo.cn",
        "Origin":"http://login.weibo.cn",
        "Referer":"http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
        "Content-Type":"application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36) (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Safari/537.36"
}
s3_header['Cookie'] = "_T_WM=%s" % s1_cookie
s3_payload = {
        "mobile":"evilfc@163.com",
        "backURL":"http%3A%2F%2Fweibo.cn%2F",
        "backTitle":"%E5%BE%AE%E5%8D%9A",
        "remember":"on",
        "tryCount":"",
        "submit":"%E7%99%BB%E5%BD%95"
}
s3_payload[pwd] = "fclove1818"
s3_payload["vk"] = vkey
r = requests.post(s3_url, headers=s3_header, data=s3_payload, allow_redirects=False)
sub = r.cookies['SUB']
gsid_CTandWM = r.cookies['gsid_CTandWM']

"""
模拟登录已经成功，需到使用到的三个Cookie值已经得到。
测试通过URL得到相关信息
"""
rm_url = "http://weibo.cn/rmrb?vt=4"
rm_header = {
        "Accept":"text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*, q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN, zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"weibo.cn",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36) (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Safari/537.36"
}
rm_header['Cookie'] = "_T_WM=%s; SUB=%s; gsid_CTandWM=%s" % (s1_cookie, sub, gsid_CTandWM)
resp = requests.get(rm_url, headers=rm_header)
page_content = resp.content
verify = Selector(text=page_content).xpath('//span[@class="ctt"]/text()').extract()
if verify[2].startswith(u"认证"):
    print "认证用户：是"
    is_verify = 1
else:
    print "认证用户：否"
    is_verify = 0

weibos = Selector(text=page_content).xpath('//span[@class="tc"]/text()').extract()
m = re.search('\d+', weibos[0])
if m:
    weibos = m.group(0)
    print "微博数：" + str(weibos)

follows = Selector(text=page_content).xpath('//div[@class="tip2"]/a/text()').extract()
m = re.search('\d+', follows[0])
if m:
    followers = m.group(0)
    print "关注数：" + str(followers)
m = re.search('\d+', follows[1])
if m:
    followees = m.group(0)
    print "粉丝数：" + str(followees)

num_weibos = 2
weibo_content = Selector(text=page_content).xpath('//div[@class="c"]/div/span[@class="ctt"]').extract()
relates = Selector(text=page_content).xpath('//div[@class="c"]/div/a/text()').extract()
clients = Selector(text=page_content).xpath('//div[@class="c"]/div/span[@class="ct"]/text()').extract()
for i in xrange(num_weibos):
    print "第%s条微博：" % str(i+1)
    print "\t" + weibo_content[i]
    m = re.findall('@', weibo_content[i])
    if m:
        print "\t@数目：" + str(len(m))
    else:
        print "\t@数目：0"
    m = re.findall('#', weibo_content[i])
    if m:
        print "\t#数目：" + str(len(m))
    else:
        print "\t#数目：0"
    m = re.findall('http://t.cn/.+', weibo_content[i])
    if m:
        print "\tURL数目：" + str(len(m))
    else:
        print "\tURL数目：0"

    flag = True
    while flag:
        if u"赞" in relates[0]:
            m = re.search('\d+', relates[0])
            if m:
                cons = m.group(0)
                print "\t赞数：" + str(cons)
            del relates[0]
            m = re.search('\d+', relates[0])
            if m:
                retweets = m.group(0)
                print "\t转发数：" + str(retweets)
            del relates[0]
            m = re.search('\d+', relates[0])
            if m:
                comments = m.group(0)
                print "\t评论数：" + str(comments)
            del relates[0]
            flag = False
        else:
            del relates[0]
    if u"客户端" not in clients[i] or u"手机" not in clients[i]:
        print "\t客户端：1"
    else:
        print "\t客户端：0"

