---
layout: post
category: 爬虫
title: 抓取漫画图片
description: 利用requests和beautifulsoup两个库来抓取关注的漫画，省得在线观看还得加载广告，浪费时间和带宽
---

平时有看漫画的习惯，数量上屈指可数，每逢想起才慢吞吞地在网上查找漫画网站阅读；但该类网站有个弊病「对个人而言」，每看一张图片得加载好多广告，既浪费时间又浪费带宽，心里颇有不爽。于是便打算利用Python抓到本地，通过电脑或者手机在碎片时间阅读。

<!-- more -->

## 思路与实现

1. 查找图片URL
2. 查找章节数or该章节总页数
3. 如何下载图片文件

此处以 [进击的巨人](http://www.57mh.com/118/)  为例子进行实操。 打开最新一话第一页，借助*浏览器开发者工具* 「F12」，查找到图片所在标签，如下

```html
<img id="manga" src="http://img.333dm.com/ManHuaKu/jinjidejuren/83/1.jpg" alt="进击的巨人漫画83话 生死抉择">
```

图片真实链接即为*src=* 那长串，尝试用浏览器直接打开上述url，发现能够正常打开，即图片能够下载。仔细观察第二页，则会发现图片的*url* 是有规律可循的，再结合总页数，你就可以把这个章节的图片下载完了。在python中如何下载图片呢？用写文件的形式即可，写入二进制文件。

```python
import requests
url = 'http://img.333dm.com/ManHuaKu/jinjidejuren/83/1.jpg'
html = requests.get(url)
data = html.content
with open('1.jpg', 'wb') as f:
    f.write(data)
```

自动寻找章节的总页数，则可以更加智能地让爬虫抓取图片，再次回到 [漫画首页](http://www.57mh.com/118/) ，观察其页面元素，最新一话的信息如下

```html
<ul style="display:block;">
  <li><a href="/118/096/" title="83话 生死决择">
      <span><i>45p</i></span>
    </a></li>
</ul>
```

章节名称，章节总页数，该有的都有了。

## 完整代码

```python
# -*- coding: utf-8 -*-

"""
下载《进击的巨人》漫画,仅适用于没用使用JavaScript加载漫画图片的网站
"""

from bs4 import BeautifulSoup
import requests


def getimgs(url):
    """
    download the pictures
    >>> getnew('http://www.57mh.com/118/096/?p=2')
    'downloading file 02-83.jpg'
    """

    html = requests.get(url)
    if html.status_code == 200:
        bs = BeautifulSoup(html.content, "lxml")
        chapter = bs.find("ul", {"style": "display:block;"})
        # 章节数
        chapter_num = chapter.li.a["title"][0:2]
        # 章节名字
        chapter_name = chapter.li.a["title"]
        # 章节总页数
        chapter_pages = chapter.li.a.span.i.string.rstrip('p')
        # 漫画名字
        # comic = bs.find_all('h1')[1].string

        pre_url = 'http://img.333dm.com/ManHuaKu/jinjidejuren'
        for i in range(int(chapter_pages)):
            # http://img.333dm.com/ManHuaKu/jinjidejuren/83/45.jpg
            img_file = '%02d-%s.jpg' % (i+1, chapter_name)
            img_url = '%s/%s/%s.jpg' % (pre_url, chapter_num, i+1)
            response = requests.get(img_url)
            if response.status_code == 200:
                print 'downloading file %s' % img_file
                with open(img_file, 'wb') as f:
                    f.write(response.content)
            else:
                print '%s can not open' % img_file
    else:
        print '%s can not open' % url

if __name__ == '__main__':
    link = 'http://www.57mh.com/118/'
    getimgs(link)
```

此处仅下载最新一话，还可以扩展代码当章节图片下载完成后打包该章节为zip文件。把脚本扔到服务器上，定期每周执行一次，有更新后即下载，再发邮件通知到自己的邮箱，实现一劳永逸。

大多数漫画网站防范意识较强，图片url并不能如此简单获取，每张图片的url地址均不同，并且使用*JavaScript*加载图片，想要抓取这类图片，则需要借用*PhantomJS* 、*Selenium* ；将来有空再更新。