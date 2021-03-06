---
layout: post
categories: 效率
title: 傻瓜式局域网文件共享
description: 简单易用的傻瓜式局域网文件共享，利用HFS这个利器便可实现
keywords: HFS, hfs, 文件共享, wifi传输
---


## **缘由**

老早就打算要写这个教程了，可忙起来时没空，有空时却又没得心思。趁着今天还有些许雅致，把这个坑给填上吧。

同事李二狗经常要我共享些文件给他，虽说可以用QQ，但有时他挂着梯子时传QQ，那速度简直不能用蛋疼来形容。他比我更懒，于是乎让我设置个共享给他，让他丫随时索取。网上查找一番windows设置共享的文章……过程我就不吐槽了，windows的共享设置别提有多复杂了。幸好让我找到一款神器，即是今天文章的主角——[HFS](http://www.rejetto.com/hfs/)，`Http File Server`。

HFS软件仅支持`WINDOWS` 平台，把你想要共享的文件通过*http协议*的方式发布出来，别人只需要在浏览器访问url即可，内网传输更具优势。

<!-- more -->

## **HFS设置**

[官网](http://www.rejetto.com/hfs/)下载软件后，安装，并运行之。界面说明如下图

<img src="/res/img/in_posts/2016-07-21_01.jpg">

什么？你觉得很复杂？

少年，听哥一句劝，运行HFS后，直接在左边的`Virtual File System` 的小房子处右键，添加文件，然后到其他设备访问顶部的地址，即可下载了。

以下的4个选项是有必要讲解的，如果你现在不知我说啥，可先行略过

- **修改端口**

直接点击顶部菜单栏的Port即可修改

- **地址栏显示IP**

点击`Open in brower` 后，浏览器显示IP而不是`localhost` ，做法是去掉`Menu` ->`Other Options` ->`browse using localhost` 的勾

- **设置开机启动**

`Menu` ->`Start/Exit` ->`Run HFS when windows start` 

- **去除`uploaded by user`**

去除某用户上传文件后，浏览器上该文件下方显示*uploaded by xxx* ， 做法是点击`Menu` ->`HTML template` ->`Edit` ，搜索`uploaded by %user%` ，删除掉这行即可

是不是很容易呢？少年

## **实际应用**

- 直接代替ftp来实现局域网文件共享

HFS支持用户管理，支持上传与删除权限，支持限速等等，当然这属于进阶部分的内容了，有兴趣的请自行研究

- 共享文件到android手机  

android设备上使用浏览器或者es资源管理器下载，我拷贝电影时就是这么干的，谁还他喵摸索数据线，再插上电脑和手机，再拷贝……别跟我提啥XX管家的XX宝不就可以内网传输么？扫描个二维码就……就你妹夫，老子可忍受不了手机上装个流氓……

- 共享文件到渣果手机 

这他喵简直就是救星啊，自从我16G的6P扔到坊间升级了128G内存后，滋长了手机看片的野心，这要放在16G时代，联想都不敢想啊。可渣果手机的机制，你懂的，播放器要钱，文件传输要用全世界最难用的itunes，呵呵。视频播放器我用的是`nplayer free` ，虽然有广告，但还能忍受，该软件内建支持浏览器下载。PDF阅读器用的是`PDF Reader` ，同样是内建支持浏览器下载，而且可以接收所有格式的文件，因为平时有手机看PDF文档的习惯，索性也就把它当作半个资源管理器了，更要命的是它还支持**WIFI传输** ，开启后甩个IP地址给别人，又可以共享文件了……

## **尾巴**

HFS的出现，如救星一般将把从水深火热的困境解救出来。对于大部分人而言均实用，毕竟瘟系统还是占主流。对比QQ、微信内网传输的优势是……不清楚……反正下载速度基本是维持5M/S这点我就满足了。软件只是一个工具而已，别让它的设定限置了用途。举个例子，每次需要推荐零食清单时，我都会用`markdown` 工具「typora」编辑好后，输出成HTML格式，添加到HFS，再华丽丽的甩个链接过去,有意向的点击标题即可跳转至原地址
<img src="/res/img/in_posts/2016-07-21_02.jpg">

那逼格，别提有多带劲了。最后的最后……

<img src="/res/img/in_posts/2016-07-21_03.jpg">

