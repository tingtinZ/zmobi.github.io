---
layout: post
title: Jekyll教程03-目录结构与主配置
category: Jekyll
description: 了解Jekyll目录结构与主配置文件的功能
keywords: Jekyll教程, 配置文件, 目录结构
---

成功地在首页上看到自己写的文章，是不是很激动呢？现在先冷静下来，平复下心情，这回来熟悉下*Jekyll* 的目录结构与主配置文件。其中，主配置文件是重点，目录结构大致记得每个目录对应着实现什么功能即可，以后在日常操作中，你会逐渐加深理解。利用好主配置文件，可以省下不少功夫。废话不多说，搬好板凳就坐，进入主题。

<!-- more -->

## 目录结构

一个基本的*Jekyll*网站的目录结构通常是这样的：

```
.
├── _config.yml
├── _drafts
|   ├── I-do-not-want-to-tell-you.md
|   └── on-simplicity-in-technology.markdown
├── _includes
|   ├── footer.html
|   └── header.html
├── _layouts
|   ├── default.html
|   └── post.html
├── _posts
|   ├── 2016-06-29-Hello-jekyll.md
|   └── 2016-04-26-install-jekyll.md
├── _site
└── index.html
```

`_config.yml` 	主配置文件，yaml格式文件，用于配置数据，详细的下面会说到

`_drafts` 		草稿，即暂未发布的文章，命名上比较随机，无须附带年月日

`_includes` 		存放用于被包含的文件，在*添加评论系统* 时再看实例

`_layout` 		存放模板文件，如前文头信息中的`layout: post` 即用文章布局

`_posts` 			你所写的文章存放处，文件名很重要： year-month-day-title.md

`_site`			执行*jekyll server* 后自动生成的目录，存放生成后的文件

`index.html` 		主页文件

`其他文件/目录` 	如自定义的资源存放目录、*data*目录、网站图标*favicon.ico*等等

## 主配置文件

