---
layout: post
title: webpy+apache+centos布署
description: 轻量级网站框架webpy在centos中使用apache的布署，补充了官网教程过去简陋的问题
category: Python
keywords: webpy, centos, apache, mod_wcgi, 
---

被邀解决轻量级网页框架`webpy` 环境的搭建，一开始我是拒绝的……没想到轻量级的就不是一样，怎么简单怎么来。它能够像 `django` 那样有个开发服务器用以调试，同理，在 *centos* 上结合 *apache* 布署也应该是同样的蛋疼！！！此话怎讲呢？请查看之前的辛酸屎——[Django+Apache+CentOS+mod_wsgi的布署]({{ site.url }}/2016/10/21/deploy-django-on-centos-with-apache) 。好吧，赶紧进入正题了。

<!-- more -->

## 基础环境

布署要求的基础环境为：

1. python 2.7.12
2. Apache 2.2.15
3. mod_wsgi 4.5.6
4. centos 6.x

`webpy` 的官方[安装文档](http://webpy.org/install#apachemodwsgi) ，直接照办即可。本文主要讲两个要点

- apache中虚拟主机的设置
- apache与webpy的关联

## 虚拟主机设置

假设我的的 *webpy* 项目在目录 `/home/your_user_name/webpy-test` ，apache配置文件为：

```shell
LoadModule wsgi_module modules/mod_wsgi.so
WSGIScriptAlias /webpy-test /home/wtadmin/webpy-test/index.py/
Listen 8080
<VirtualHost *:8080>
    LogLevel debug
  
    Alias /webpy-test/media/ /home/your_user_name/webpy-test/media/
    Alias /webpy-test/static/ /home/your_user_name/webpy-test/static/
        AddType text/html *.py
  
    <Directory "/home/your_user_name/webpy-test">
                #AllowOverride all
                Options Indexes FollowSymLinks ExecCGI
        Order deny,allow
                SetHandler wsgi-script
        Allow from all
    </Directory>
</VirtualHost>
```

它与其他 *apache* 虚拟主机配置不一样的地方在于，并不需要指定 *ServerName* ，*DocumentRoot* 之类的东东；直接在开头的 *WSGIScriptAlias* 声明好即可。

## apache+webpy关联

按上述配置好之后，浏览器访问 `http://your_ip:8080/webpy-test` ，apache日志提示如下（除去目录访问权限的问题）

```shell
ImportError: No module named setting
# 或者是
ImportError: No module named web
```

原因是 *apache* 访问 *index.py* 之后，无法导入XX模块，因为找不到相应的路径，[官方安装说明](http://webpy.org/install#apachemodwsgi) 上也有提到。

```python
# 在index.py中import web之前添加
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
```

这回可以找到相应的模块了，但还是无法启动，提示

```shell
Target WSGI script '/home/your_user_name/webpy-test/index.py' \
does not contain WSGI application 'application'.
```

原因是 *apache* 执行了index.py，但无法用自身加载的 *mod_wsgi* 模块来执行，即两者没关联到。

```python
# 在index.py最后添加以下两句
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
```

再试试看？嘿嘿……