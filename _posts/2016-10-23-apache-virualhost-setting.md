---
layout: post
title: Apache多域名与多IP虚拟主机设置
description: apache中多域名与多IP虚拟主机的设置，注意apache2.2 与 apache2.4之间的区别
category: Apache
keywords: Apache, 多域名, 多IP， 虚拟主机

---

在Apache中设置多域名与多IP的虚拟主机，不同的版本之间有小小的区别。仅以此文做留存处理，方便以后查找追溯。Apache目前主要的版本区别为 *2.2* 与 *2.4* ；较新的系统上（如ubuntu）使用的均是2.4版本，而*CentOS* 等以稳定性著称的系统则坚守着2.2版本。另外，MacOS上的apache又有小小的区别。

<!-- more -->          

## Apache权限设置

*Apache 2.2*  中，设置权限的语句为

```shell
Order deny, allow
Allow from all
```

*Apache 2.4* 中，设置权限的语句为

```shell
Require all granted
```

## 多域名虚拟主机

新建两个虚拟主机配置，分别为*web.conf* 与  *blog.conf* ，详细配置分别为

```shell
# web.conf
<VirualHost *:80>
	ServerName web.test.com
	ServerAlias web.test.com
	DocumentRoot "/data/web"
	<Directory "/data/web">
		Order deny,allow
		Allow from all
	</Directory>
</VirualHost>
```

```shell
# blog.conf
<VirualHost *:80>
	ServerName blog.test.com
	ServerAlias blog.test.com
	DocumentRoot "/data/blog"
	<Directory "/data/blog">
		Order deny,allow
		Allow from all
	</Directory>
</VirualHost>	
```

注意：在 apache2.2版本中，需要在 `/etc/http/conf/httpd.conf` 中把启用这条记录

```shell
NameVirtualHost *:80
```

如果只是在本地测试，则需要在本地hosts文件中添加域名解析

```shell
127.0.0.1 web.test.com
127.0.0.1 blog.test.com
```

如果是在公网上使用，则需要自行添加域名解析。

如果你的虚拟主机项目主目录均在同一父目录下，则可以使用`rewrite`模块来快速实现二级域名的设置，详情可参考[Apache rewrite_mod]({{ site.url }}/2016/10/24/apache-mod_rewrite-usage.html)

## 多IP虚拟主机

这个就简单多了，直接把虚拟主机配置中的 `<VirualHost 'your_ip':80>` 即可。

## 其他

当然，如果你不要求使用80端口，则可以自行建立以其他端口为监听的虚拟主机。有个细节需要注意，即在虚拟主机配置时，需要额外指定你所想要监听的端口

```shell
Listen '你想要监听的端口'
<VirutalHost *:'你想要监听的端口'>
```

最后，谈谈 *apache* 新旧版本之间的哲学吧……旧版以集中处理为原则，相反，新版 则是相对分散，从易用性的角度来看，新版更占优势。来看看两者的目录结构吧

```shell
# /etc/httpd   apache 2.2
.
├── conf
├── conf.d
├── logs -> ../../var/log/httpd
├── modules -> ../../usr/lib64/httpd/modules
└── run -> ../../var/run/httpd
```

```shell
# /etc/apache2 apache 2.4
.
├── apache2.conf
├── conf-available
├── conf-enabled
├── envvars
├── magic
├── mods-available
├── mods-enabled
├── ports.conf
├── sites-available
└── sites-enabled
```