---
layout: post
category: Python
title: 使用Python实现JPG转PDF
description: 在python中使用reportlab库把漫画JPG图片转换成PDF
keywords: python, jpg, pdf, reportlab, jpg convert pdf, JPG转PDF
---

[抓取漫画图片]({{ site.url }}/2016/07/23/get-comic-img.html)完毕后，倘若要在手机上阅读，则需要转成PDF。部分手机PDF软件支持直接浏览图片的，但这种方式个人不太接受罢了。刚好今天有漫画更新，下载完毕，打算直接生成PDF，借助Python的`reportlab`库实现。

<!-- more -->

## 实现代码

使用PIP安装库： `pip install reportlab`

我下载好的漫画图片在当前目录，命名格式为 *「页数-章节名称.jpg」*

接着是详细的代码

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.units import inch
import commands

# 获取所有图片名字
img_names = commands.getoutput('ls *.jpg')
# 存储读取图片后的信息
pages = []
width = 7.5*inch
height = 9.5*inch
# 待输出的PDF文件名
pdf_file = '84话-白夜-进击的巨人.pdf'
# 实例化模板对象，用于生成pdf文件
doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
# 读取每张图片信息
for img in img_names.split('\n'):
    data = Image(img, width, height)
    pages.append(data)
    pages.append(PageBreak())
# 生成PDF文件   
doc.build(pages)
```

此番操作的优点吧

1. 摆脱了平台与软件的限制
2. 不必打包成zip

> [参考网文](http://www.blog.pythonlibrary.org/2012/01/07/reportlab-converting-hundreds-of-images-into-pdfs/)
