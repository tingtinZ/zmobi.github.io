---
layout: post
title: Apache使用mod_rewrite
category: Apache
description: 在apache中开启mod_rewrite，使之支持重定向，重新定义链接等等功能
keywords: apache, mod_rewrite, redirect, remapping, 重定向, 重写, 二级域名
---

*apache mod_rewrite* 是个非常强大的模块，它提供了一种能够管理URL的方法。通过该模块，你几乎可以重写所有你想要的URL。但它的复杂程序对于入门者来说，似乎非常有难度。它主要使用了正则来构建其语法，下面将简单介绍下这个*mod_rewrite* 。

<!-- more -->      

## Rewrite 基本规则

一个重写规则包含三个参数，以空格作为分隔符。这三个参数分别是

1. Pattern —— 使用正则编写的过滤条件
2. Substitution —— 匹配后的真实请求地址
3. Flags —— 标志位，它能够影响到重写后的请求

<img src="/res/img/in_posts/syntax_rewriterule.png" >

`Substitution` 可以是以下几种形式

#### 替代绝对路径

```shell
RewriteRule "^/games" "/usr/local/games/web"
```

效果与 *alias* 别名类似，但我自己实践时却出不来效果，暂时无解。

#### 替代web访问路径

```shell
RewriteRule "^/foo$" "/bar"
```

假设网站根目录设置为 */var/www/html* ，则访问你设置的网站 *http://example.com/foo* 则会自动访问至实际目录 */var/www/html/bar* 。

大爷的，我实践过程中，仍然出不来，暂时无解。

#### 替代为别的网站链接

```shell
RewriteRule "^/admin$" "http://site2.example.com/admin.html" [R]
```

这个很好理解，即设定替代规则，当访问你的网站 *http://example.com/admin* 则自动跳转至别的网址 *http://site2.example.com/admin.html* 。这个实践时能出来效果。当初为了赶时间，弄了个django后台，链接只能是 *域名/admin* 来访问；可上面要求得是 *http://admin.xxx.com* 直接进入后台，没办法，只能以这种取巧的方式来实现咯。

#### 替代规则中包含正则

```shell
RewriteRule "^/product/(.*)/view$" "/var/web/productdb/$1"
```

变量 *$1* 即为 *pattern* 中匹配到的名字，例如访问 *http://example.com/product/check/view* 则会访问目录 */var/www/html/productdb/check* 。

## Rewrite Flags

此处不对*flags* 进行展开，详情可参考 [官方文档](http://httpd.apache.org/docs/current/zh-cn/rewrite/flags.html) 与 [网友文档](http://lesca.me/archives/htaccess-appendix.html#htaccess_regex)

## Rewrite 条件

*Rewrite Conditions* ，相当于是编程语句中的条件判断，我们在上述的基本规则中谈到的更改，只能应付些简单的替代需求 ，当遇到复杂的替代需求时，得 *conditions* 上场了。

它同样包括三个参数，可参看下图。第一个参数通常是web服务上的系统变量名；第二个才是真正的条件语句，第三个则依然是 *flag* 。

<img src="{{ site.url }}/res/img/in_posts/syntax_rewritecond.png">

## Rewrite Maps

在 [Apache多域名与多IP虚拟主机设置]({{ site.url }}/2016/10/23/apache-virualhost-setting.html) 一文中提到的二级域名快速设定，使用的便是 重写映射。详细的说明可参考 [官方文档](http://httpd.apache.org/docs/current/zh-cn/rewrite/rewritemap.html) ；此处只讲解二级域名设定。

需要注意的是，二级域名的设定有个前提条件，必须在同一父目录之下，即网站根目录为 */var/www/html* ，其他网站根目录为 */var/www/html/blog* ， */var/www/html/book/* 。在*/var/www/html* 对应的配置文件中，添加如下内容

```shell
RewriteEngine on
RewriteMap lowercase int:tolower  # 参考官方文档，有四种类型
RewriteMap vhost txt:/etc/apache2/vhost.map # 设定重映射的配置文件
RewriteCond ${lowercase:%{SERVER_NAME}} ^(.+)$ 
RewriteCond ${vhost:%1} ^(/.*)$ 
RewriteRule ^/(.*)$ %1/$1 # 
```

`vhost.map`

```shell
www.example.com /var/www/html
blog.example.com /var/www/html/blog
book.example.com /var/www/html/book
```

## .htaccess files

此处不对 *.htaccess* 进行展开，详情可参考 [官方文档](http://httpd.apache.org/docs/current/zh-cn/howto/htaccess.html) 与 [网友文档](http://lesca.me/archives/htaccess-rewrite.html)

## 小结

此处只是做了个简单的介绍，并未展开深入的研究探讨，鉴于时间因素，日后再做详细展开。

> [Apache mod_rewrite 简介 ](http://httpd.apache.org/docs/current/zh-cn/rewrite/intro.html)
>
> [使用RewriteMap](http://httpd.apache.org/docs/current/zh-cn/rewrite/rewritemap.html)
>
> [.htaccesss技巧：URL重写与重定向](http://lesca.me/archives/htaccess-rewrite.html)
>
> [Flag详解](http://lesca.me/archives/htaccess-appendix.html#htaccess_regex)
