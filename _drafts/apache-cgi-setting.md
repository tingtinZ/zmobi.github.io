---
layout: post
category: Apache
description: ubuntu下Apache的配置，主要是CGI配置，使用python脚本
title: Apache2.4在ubuntu的cgi配置
keywords: apache2.4, ubuntu, cgi, python
---

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
添加虚拟主机配置时，记得在要首行添加监听端口，否则无法正常使用配置
Listen 端口号 
