---
layout: post
category: ['Python', 'Apache']
title: Apache2.4配置Python CGI
description: 在apache2.4中配置python cgi，包括windows、macos和linux三大系统的配置说明
keywords: python, CGI, apache2.4, macos, osx, linux, windows
---

因工作需要，外加自身实践过程中需要经常切换不同的环境来检验。不同的操作系统，apache配置文件也有异同，配置过程略为烦琐，花了不少时间折腾。遂抽空把它们在集结在一块记录下来，方便日后使用，节省时间。

<!-- more -->

# Windows系统

## 下载apache2.4

鉴于apache官方网站没有win的安装包，因此在[另外的网站](https://www.apachelounge.com/download/)找到压缩包，解压即可使用。

## Apache配置

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


# MacOS系统


*MAC* 下的python cgi配置与此类似，但有点小区别，mac可以指定个人家目录下的`Sites`为网站主目录。废话不多说，以下是具体配置。

P.S: 访问个人目录的url为：**http://127.0.0.1/~your_name/xxx.html**


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
<Directory "/Users/your_name/Sites/">
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


# Ubuntu系统


在ubuntu16.04环境下，使用`sudo apt install apache`安装，在内网中调试使用时，需要做的更改有：


1、添加ServerName

`echo ServerName 127.0.0.1 >> /etc/apache/apache.conf`


2、修改支持cgi的配置


```shell
# 在配置 sites-available/000-default.conf 中添加
ScriptAlias /cgi-bin/ /var/www/html/cgi-bin/

# 在加载模块 mods-available/mime.load  中添加
LoadModule cgi_module /usr/lib/apache2/modules/mod_cgi.so
```


3、Apache常用命令

```shell
apache2ctl [ start | stop | restart | reload ]
a2enconf 启用配置  
a2enmod  启用模块   
a2ensite 启用网站
同理，禁用的话，则把en改为dis
```


4、注意事项

添加虚拟主机配置时，分两种情况：

1. 如果继续沿用80端口，则要在配置文件中添加 *ServerName xxxx*，然后在本地做域名解析，通过域名来访问
2. 使用新的端口，则在配置文件首行添加 *Listen 端口号* 
