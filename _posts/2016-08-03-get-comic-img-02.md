---
layout: post
category: 爬虫
title: 抓取漫画图片「二」
description: 借助PhantomJS和Selenium实现等待页面加载完成后，获取真实漫画图片url，再进行下载
keywords: phantomjs, selenium, python, 爬虫, 漫画
---

在[上一篇文章]({{ site.url }}/2016/07/23/get-comic-img.html) 的末尾处提到，某些漫画网站会使用*JavaScript* 来动态加载漫画图片，如果按照之前的套路，简单抓取下来，再用**美丽汤**去解析，查找图片*URL* 时，则结果为空。为什么呢？那便是*JavaScript* 的功能呗。

使用*chrome*打开漫画的某一章节某一页时，借助*开发者工具* 查看完整的页面加载过程，你会看到加载时间略长，并且80%左右的时间都用来加载广告图片。本质上页面加载过程分为两个步骤，一是加载基本的框架，如在哪里放置哪些资源，是图片还是文字；二是浏览器执行页面上的*javascript* 把图片等其实数据加载成功。如此一来，页面才是完整地展示在你面前。

<!-- more -->

## 在Python中用Selenium执行JavaScript

*Selenium* 是一个强大的网络数据采集工具，其最初是为网站自动化测试而开发的。近几年，它还被广泛用于获取精确的网站快照，因为它们可以直接运行在浏览器上。Selenium 可以让浏览器自动加载页面，获取需要的数据，甚至页面截屏，或者判断网站上某些动作是否发生。

Selenium 自己不带浏览器，它需要与第三方浏览器结合在一起使用。例如，如果你在 Firefox 上运行 Selenium，可以直接看到一个 Firefox 窗口被打开，进入网站，然后执行你在代码中设置的动作。虽然这样可以看得更清楚，但是我更喜欢让程序在后台运行，所以我用一个叫 [PhantomJS](http://phantomjs.org/download.html)的工具代替真实的浏览器。

PhantomJS 是一个“无头”（headless）浏览器。它会把网站加载到内存并执行页面上的 JavaScript，但是它不会向用户展示网页的图形界面。把 Selenium 和 PhantomJS 结合在一起，就可以运行一个非常强大的网络爬虫了，可以处理 cookie、JavaScrip、header，以及任何你需要做的事情。

Selenium可以使用pip安装，而PhantomJS则需要到[官网](http://phantomjs.org/download.html) 根据自身平台情况下载。

以《Python网络数据采集》一书中的例子来辅助讲解。作者建了一个 [Demo](http://pythonscraping.com/pages/javascript/ajaxDemo.html) 页面，打开页面2秒后，页面就会被替换成一个 Ajax 生成的内容。如果我们用传统的方法采集这个页面，只能获取加载前的页面，而我们真正需要的信息（Ajax 执行之后的页面）却抓不到。

使用下面的代码来获取加载后的内容

```python
from selenium import webdriver
import time

# 指定你的PhantomJS所在路径
driver = webdriver.PhantomJS(executable_path='your_phantojs_path')
url = "http://pythonscraping.com/pages/javascript/ajaxDemo.html"
driver.get(url)
time.sleep(3)
print driver.find_element_by_id('content').text
# 此步很重要
driver.close()
```

## 实战演练

**背景说明**

```txt
下载作品： All You Need Is Kill 「明日边缘-漫画」
下载来源： http://www.57mh.com/3680/
```

**实现思路**

1. 先获取章节数与每章节总页数 「*getchapter*」
2. 使用循环遍历每页，获取图片真实url 「*geturl*」
3. 使用write二进制文件下载图片 「w2f」

**完整代码**

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
from os import path
from random import randint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/52.0.2743.82 Safari/537.36'
}


def getchapter(url):
    total = {}
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        bs = BeautifulSoup(html.content, "lxml")
        # 查找包含所有章节的元素
        items = bs.find("ul", {"style": "display:block;"}).find_all("span")
        for item in items:
            # <span>17\u8bdd<i>23p</i></span> 选出章节和总页数
            result = re.match(re.compile('.*?(\d{2}).*?(\d{2})p'), str(item))
            chapter = result.group(1)
            pages = result.group(2)
            print '第%s章 总%s页' % (chapter, pages)
            total[int(chapter)] = int(pages)
        return total
    else:
        print '网页 %s 无法打开' % url


def geturl(url, info):
    for chapter in info:
        # 添加判断条件，可自主控制下载的章节
        if chapter >= 1:
            # 指定phantomjs所在路径
            driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
            if chapter >= 10:
                chapter_url = '%s%03d/' % (url, chapter)
            else:
                chapter_url = '%s%02d/' % (url, chapter)
            for num in range(1, info[chapter]+1):
                # 拼装成完整的单个章节每页的URL
                page_url = '%s?p=%d' % (chapter_url, num)
                # 关键实现之处
                driver.get(page_url)
                html = driver.page_source
                # 暂时先借助美丽汤来解释页面信息
                bs = BeautifulSoup(html, "lxml")
                # 图片真实url
                img_url = bs.find('img', {'id': 'manga'})["src"].split('=')[1]
                # 图片后缀名
                suffix = img_url.split('.')[-1]
                # 生成图片文件的名字
                img_name = '%02d-%02d.%s' % (chapter, num, suffix)
                print '正在下载 第%d章 第%d页' % (chapter, num)
                w2f(img_url, img_name)
                time.sleep(randint(10, 24))
            driver.close()


def w2f(real_url, filename):
    directory = '下载到哪个目录'
    full_name = path.join(directory, filename)
    if path.isfile(full_name):
        pass
    else:
        html = requests.get(real_url, headers=headers)
        if html.status_code == 200:
            with open(full_name, 'wb') as f:
                f.write(html.content)
        else:
            print '图片 url %s 无法打开' % real_url
        time.sleep(randint(1, 10))

if __name__ == '__main__':
    link = 'http://www.57mh.com/3680/'
    chapter_pages = getchapter(link)
    geturl(link, chapter_pages)
```

通过上述代码，本人成功下载完整的章节，`存在问题`有，使用`driver.get(url)`时，偶尔会等待好久，卡死了，只能重新开始，暂时没找到解决方法，虽然机率较小。在*windows*上使用`FSCapture` 把所有图片转成*PDF*格式，可以爽了。下载的过程中，勿盲目求快，否则过度占用他人资源，可耻也；这也是加入随机等待的原因。

至于`Selenium`和`PhantomJS`的学习过程，有空再写个总结。并非使用上述技能就万事大吉了，仍然存在某些漫画网站，即便成功获取图片真实URL也无法下载，可能与*Cookies* 和 *Session* 的处理有关，以后再慢慢补充。