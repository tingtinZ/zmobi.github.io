---
layout: post
category: 爬虫
title: 抓取cnbeta新闻
description: 通过requests库和美丽汤抓取cnbeta新闻，过滤掉广告与图片，对感兴趣的文章再跳转到原文查看
keywords: cnbeta, 爬虫, 简洁新闻, python
---

作为IT狗，平时有阅读科技新闻的习惯，会经常逛逛*cnbeta*网站，每次看到那些脑残、野蛮推广的页游广告极为烦躁，巧好前几天有简单学习了点*python* 爬虫的知识，遂打算动手弄个简洁版的新闻网页。

<!-- more -->

### 思路整理

1. 获取主页上每篇文章的URL
2. 访问文章URL，抓取正文信息

首先借助**chrome**的开发者工具，快捷键是`F12`，查看cnbeta首页的页面元素，依次查看html结构

```html
<html>
  <head>
    <title>www.cnbeta.com</title>
  </head>
  <body>
    <section class="wrapper">
      <div class="main_content">
        <div class="content_box main_content_left">
          <div class="mt5 allinfo">
            <!-- 我在这里 -->
            <div class="all_news_wildlist">
            </div>
          </div>
        </div>
      </div>
    </section>
  </body>
</html>
```

到这里，能够看到一个ID为`allnews_all`的标签，文章列表就隐藏在这里了。我们需要的信息就只有这个

```html
<a target="_blank" href="/articles/524617.htm">网速持续提升 报告称中国宽带已迎来“10M时代”</a>
```

`href`标签中的*URL*链接而已。

接着到单独的文章页面以同样的方法查看页面元素，则会发现文章的摘要和正文信息

```html
<!-- 摘要信息-->
<div class="introduction"></div>

<!-- 正文信息 -->
<div class="content"></div>
```

注意：摘要+正文才是完整的文章。

### 具体实现

- 使用requests访问

```python
import requests
header = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
}
url = 'http://www.cnbeta.com'
html = requests.get(url, headers=header)
```

- 使用美丽汤获取信息

```python
from bs4 import BeautifulSoup
import re
# 将上述请求结果扔到美丽汤
bs = BeautifulSoup(html.content, "html.parser")
# 获取所有文章链接，再逐个遍历，形成完整的URL
items = bs.find_all("div", {"class": "title"})
	for item in items:
        print 'url is %s' % url + item.a["href"]
 
# 如果访问的链接是具体某篇文章，则标题、摘要和正文分别是
title = bs.h2.string
summary = bs.find('div', {'class': 'introduction'}).p.get_text()
article = bs.find_all('p', {'style': re.compile('text-align: .*?left;')})
```

### 完整代码

访问cnbeta主页，获取40篇文章，每篇文章单独一个*MarkDown* 文件

```python
# -*- coding:utf-8 -*-

import re
import requests
import sys
import time
from os import path as path
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}


def w2f(content):
    """
    >>> w2f('hello world')
    'finished wrote fucking'
    """
    post_dir = '/home/jeff/jtest/_posts'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    now = time.strftime("%Y-%m-%d-%H%M%S")
    md_file = path.join(post_dir, '%s.md' % now)
    with open(md_file, 'w+') as f:
        for line in content:
            f.write(line)
    print 'finished wrote fucking  %s.md' % now
    time.sleep(2)


def getinfo(url, ver=None):
    """
    >>> purl = getinfo('http://www.cnbeta.com')
    """
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        bs = BeautifulSoup(html.content, "html.parser")
        if ver is None:
            purl = []
            items = bs.find_all("div", {"class": "title"})
            for line in items:
                purl.append(url+line.a["href"])
            return purl
        else:
            content = []
            title = bs.h2.string
            summary = bs.find('div', {'class': 'introduction'}).p.get_text()
            article = bs.find_all('p', {'style': re.compile('text-align: .*?left;')})
            # 添加jekyll文章表头信息
            content.append('---\nlayout: post\ncategory: News\ntitle: %s\n---\n' % title.replace('[]', ''))
            # 添加阅读原文
            content.append('[阅读原文](%s)\n\n' % url)
            content.append('%s\n\n' % summary)
            # 添加 read more 标签
            content.append('<!-- more -->\n\n')
            for line in article:
                content.append('%s\n\n' % line.get_text())
            w2f(content)
    else:
        print 'url %s can not interview' % url

if __name__ == '__main__':
    link = 'http://www.cnbeta.com'
    urls = getinfo(link)
    for item in urls:
        getinfo(item, ver='single')
```

获取上述文章主要是用来辅助学习Jekyll静态博客的。可以修改成在同一个*MarkDown*文件中展示，页面最上方显示文章列表，点击感兴趣的新闻，跳转到该页面中文章的位置，阅读时如果想跳转至原网页，点击标题即可，代码实现这里就不贴了。

有空再把`requests`和`BeautifulSoup`的内容补上。

> [requests中文文档](http://cn.python-requests.org/zh_CN/latest/)
>
> [BeautifulSoup中文文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)

