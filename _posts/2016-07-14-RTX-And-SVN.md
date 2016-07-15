---
layout: post
categories: svn
title: SVN绑定RTX发送即时消息
description: SVN绑定RTX通过HTTP发送即时消息，当SVN有提交时，马上发送RTX弹窗消息通知指定人群
keywords: svn, rtx, http, hooks
---

反复琢磨了好几次，终究是想不出一个简洁又能清晰表达立意的标题，瞧我这语文水平，啧啧。公司有同学在网上看到类似的功能：*当某人在SVN提交更新后，RTX立即发送弹窗通知指定人群*！ 经过一个下午时间的调研，把整个流程理顺并且实现了该功能，关键点在于两个：**SVN的hooks** ，**RTX的http消息** 

实验环境  **SVN Server： VisualSVN Server  in windows 7** 

<!-- more -->

#### Part.One :  RTX

- 安装*RTX*的*sdk* 

在rtx服务端所在机器上安装rtx的sdk，或者直接完整安装RTX服务端即可。在安装的根目录上使用*notepad++*打开文件`SDKProperty.xml`，按照以下格式修改

```xml
<?xml version="1.0"?>
<Property>
<APIClient>
	<IPLimit Enabled="1">
		<IP>127.0.0.1</IP>
         <!-- 我是新添加的IP -->
		<IP>10.0.0.122</IP>
	</IPLimit>
</APIClient>
<sdkhttp>
    <!-- 将原有值1改成0 -->
	<IPLimit Enabled="0">
	</IPLimit>
</sdkhttp>
</Property>
```

如果有多个IP地址，则所有都需要添加上！

- 开启服务

按`win+r`键，输入 **services.msc** ，重启这两个服务：`RTX_HTTPServer`和`RTX_SvrMain`

> 当初折腾时，网上的文章完全没人提到这两个服务，心好累，特别是RTX_HTTPServer没开启，无法使用8012这个端口

- 测试消息

在添加IP所在的主机「*此处为10.0.0.122*」，浏览器中访问：

`http://rtx_server_ip:8012/SendNotify.cgi?msg=hello&receiver=yourname`，此时电脑右下角会有消息弹窗

- 发送中文消息

你是不是很*机智*的想使用`中文` 来进行上面的测试呢？哈哈！发现右下角的弹窗中文会显示乱码对吧？此时你需要在RTX所在服务器上修改文件`SendNotify.cgi` 

```php
// 大概在第29行的空白位置插入以下三行内容
$msg = iconv("utf-8","gbk", $msg); 
$title = iconv("utf-8","gbk", $title);
$receiver = iconv("utf-8","gbk", $receiver);
```

重启服务`RTX_HTTPServer` 后再发条消息试试看吧。

#### Part.Two : SVN

- SVN Hooks

什么是*SVN HookS* 呢？其实它是由svn提供的一组由svn**事件触发**的特别有用的程序。这些程序在服务器端执行，可以提供svn之外的一些附加功能。钩子可以调用批处理文件、可执行文件或者一些类似于`perl`、`python` 等的脚本。

回归到本文的需求，当某人提交更新这个事件后，再触发下一步动作，因此则选取`post-commit` 提交后的钩子。在svn server机器上，进入待设置钩子的仓库目录，在`hooks` 目录下，把默认的`post-commit.tmpl` 文件重命名为`post-commit.bat` ，这样SVN在提交后才会自动执行该脚本。`post-commit.bat` 内容为

```bat
:: 我是注释，请勿复制
echo off
d:
cd 待设置的仓库目录\hooks
start C:\Python27\python 你所写的python脚本
exit
```

钩子设置好之后，问题又来了，脚本怎么写？

- 获取SVN提交信息的python脚本

网上能找到的大多是BAT批处理脚本，虽然能粗略看懂，但本人未涉猎过bat，遂考虑以python来写，废话不多说，直接上脚本

```python
# -*- coding:utf-8 -*- 

import urllib2
import os

# 在系统环境变量中加入路径 "C:\Program Files\VisualSVN Server\bin"
MainPath = r'd:\Repositories'  # 这是我的SVN SERVER目录，请更改为自己的
path = os.path.join(MainPath, 'CangKu')
# 获取SVN提交者的人名
name = os.popen('svnlook author '+str(path)).read().rstrip('\n')
# 获取SVN提交的版本号
ver = os.popen('svnlook youngest '+str(path)).read().rstrip('\n')
# 获取SVN提交时的路径名
dirs = os.popen('svnlook changed '+str(path)).read().rstrip('\n')
# 获取SVN提交时所写的注释
log = os.popen('svnlook log '+str(path)).read().replace(' ','').rstrip('\n')
# 中文注释使用chardet模块，调用chardet.detect(log)才最终确认是gb2312编码
log = log.decode('gb2312').encode('utf-8')

# 发给所有人则直接令 receiver = all即可
receiver = 'rtx_user_name'
# 因SVN Server上每个仓库只显示一个层级，若想指定下属的某个目录更新时才触发消息通知
# 则可以添加条件判断路径名
if 'keyword' in dirs:
    # msg的内容不能有空格或者其他符号，不然显示不全，因此排版略蛋痛
    msg = '【%s】向仓库【release/win】提交了【版本号：%s】的更新【%s】' %(name, ver, log)
    url = 'http://rtx_server_ip:8012/SendNotify.cgi?delaytime=4000&receiver=%s&msg="%s"' %(receiver, msg)
    # 使用urllib2.urlopen方法来模拟浏览器访问
    urllib2.urlopen(url)
```

为脚本命个名字吧，再添加到`post-commit.bat` 文件中即可。

现在提交个更新测试效果吧

*参考文章* 

> [SVN绑定RTX 即时提醒](http://blog.csdn.net/yong_sun/article/details/8239631)
>
> [SVN HOOKS钩子详解](http://www.uml.org.cn/pzgl/201204262.asp)
>
> [RTX发送消息时注意事项](http://www.cnblogs.com/SanMaoSpace/p/4983263.html)
