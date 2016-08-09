---
layout: post
categories: jekyll
title: Jekyll显示文章摘要
description: 使用jekyll搭建github page博客时如何在首页中显示文章摘要呢？其实官方的做法是excerpt
keywords: jekyll,excerpt,github,blog
---


解决完设置`多说` 评论后，在闲暇时间查找关于*jekyll博客文章设置显示摘要* ，这不得不吐槽天朝内的搜索引擎真他喵的**辣鸡** ，净是些乱七八糟而又没营养的东西。

<!-- more -->

原有`index.html`中，有这样的一行：

```html
{{ post.content || split:'<!-- more -->' | first }}
```

不知道若要显示文章摘要，需要在*_Post* 下的文章里，按自己所需的位置添加`<!-- more -->` 即可。

- 官方推荐：excerpt

在`_config.yml`文件中，添加指定摘要的分隔符

```html
excerpt_separator: '<!-- more -->'
```

通常情况下，摘要需要去掉html标签，因此改为

```html
{{ post.excerpt | strip_html }}
```

在你书写文章时，按自己的想法添加`<!-- more -->`吧。

如果还不理解，请查看 [我的项目主页](https://github.com/zmobi/zmobi.github.io) 吧

- 存在问题

打开首页时，虽然能显示摘要，但不能渲染成*markdown* 的格式，等哪天有空时再弄吧

> 参考：[jekyll显示文章摘要](http://www.cnblogs.com/coderzh/p/jekyll-readmore.html)

