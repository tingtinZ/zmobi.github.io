---
layout: post
title: CentOS中安装Django
category: Django
description: CentOS中如何以源码方式安装Django呢？需要注意的地方有哪些呢？容老夫细细道 来
keywords: django, centos, 源码安装django
---

在ubuntu下安装django非常方便，直接跑apt命令即可。这要换到centos环境下就略为蛋疼了。只能以源码方式安装，并且安装前还得注意环境的配置。

<!-- more -->


## 以下是详细的安装过程


### python升级
由默认的2.6.6 升级到 python2.7，安装完成后，先别急着清理安装目录，一会还得再用

```shell
# 下载安装python2.7.12
cd /usr/src
wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
tar -xf Python-2.7.12.tgz
cd Python-2.7.12
./configure --prefix=/usr/local
make all
make install

# 替换原换文件，并解决Yum依赖2.6.6的问题
mv /usr/bin/python /usr/bin/python2.6.6
ln -s /usr/local/bin/python2.7 /usr/bin/python
sed -i 's/python/python2\.6\.6/g' /usr/bin/yum
```


### 安装pip与easy_install
注意安装的先后顺序，必须先安装easy_install，否则pip无法安装

```shell
# easy_install
wget https://bootstrap.pypa.io/ez_setup.py -O - | python

# pip
wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14a\
eff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#\
md5=87083c0b9867963b29f7aba3613e8f4a
tar -xf pip-8.1.2.tar.gz
cd pip-8.1.2
python setup.py install

# bpython，这个力荐安装
pip install bpython
# 如果pip安装失败，则
easy_install bpython
```


### 安装django
此处需注意，解决sqlite模块不存在的问题

```shell
# 安装django
wget https://www.djangoproject.com/m/releases/1.10/Django-1.10.1.tar.gz
tar -xf Django-1.10.1.tar.gz
cd Django-1.10.1
python setup.py install 

# 安装sqlite
yum -y install sqlite-devel

# 进入python2.7的安装目录，重新安装python2.7,把sqlite3模块添加进来
cd /usr/src/Python2.7.12
make install
```

安装完毕，赶紧新建一个django项目来测试下`python manager runserver`吧
