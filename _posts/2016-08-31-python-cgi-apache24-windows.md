---
layout: post
category: Python
title: Python CGI With Apache2.4 in windows
description: 在windows下搭建apache服务，并开启cgi模式，支持解释python
keywords: python, CGI, apache2.4, windows
---

因工作需要，在内网window机器上搭建个apache，以网页形式执行某些操作，遂把搭建过程简单记录下，以备查。

<!-- more -->

### 下载apache2.4

鉴于apache官方网站没有win的安装包，因此在[另外的网站](https://www.apachelounge.com/download/)找到压缩包，解压即可使用。

### Apache配置

本人打算把apache放在D盘，因此`httpd.conf`中需要做如下修改


```shell
ServerRoot "d:/Apache24"

# 按需求而定
Listen 8080

# 确保mod_cgi.so没注释掉
LoadModule cgi_module modules/mod_cgi.so  

# 无域名的话，可暂时用本地ip
DocumentRoot "d:/Apache24/htdocs"

<Directory "d:/Apache24/htdocs">

Options Indexes FollowSymLinks ExecCGI

ScriptAlias /cgi-bin/ "d:/Apache24/cgi-bin/"

<Directory "d:/Apache24/cgi-bin">

AddHandler cgi-script .cgi .py
```


### 测试时的要点


在`cgi-bin`目录下新建*python*脚本时，需要注意，一定要指明解释器的路径和打印的类型

```python
#! C:\Python27\python.exe
# -*- coding: utf-8 -*-
print "Content-type: text/html\r\n\r\n"
print '<h1>hello, fuck you</h1>'

# 以下是检测浏览器环境信息的
import os
 
print "Content-type: text/html\r\n\r\n";
print "<font size=+1>Environment</font><\br>";
for param in os.environ.keys():
  print "<p><b>%20s</b>: %s</p>" % (param, os.environ[param])
```


### 挤挤更健康


*MAC* 下的python cgi配置与此类似，但有点小区别，mac可以指定个人家目录下的`Sites`为网站主目录。废话不多说，以下是具体配置。

```shell
mkdir -pv ~/Sites


vim /etc/apache2/httpd.conf
# 取消注释
LoadModule userdir_module libexec/apache2/mod_userdir.so
LoadModule cgi_module libexec/apache2/mod_cgi.so

# 更改ServerName
ServerName 127.0.0.1:80

# 日志改为debug 以便排错
LogLevel debug

# 添加*.py的支持
AddHandler cgi-script .cgi .py

# 支持额外的用户配置
Include /private/etc/apache2/extra/httpd-userdir.conf


# apache中个人目录配置
vim /etc/apache2/users/your_name.conf
<Directory "/Users/jeff/Sites/">
    Options Indexes MultiViews ExecCGI
    AllowOverride all
    Require all granted
</Directory>


# *.py文件放在Sites目录下即可，来个检测浏览器环境的脚本吧
# 以下是文件内容

#! /usr/bin/env python
import os
 
print "Content-type: text/html\r\n\r\n";
print "<font size=+1>Environment</font><\br>";
for param in os.environ.keys():
    print "<p><b>%20s</b>: %s</p>" % (param, os.environ[param])
```
