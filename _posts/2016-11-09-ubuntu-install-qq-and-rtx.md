---
layout: post
title: ubuntu16.04安装QQ与RTX
description: 如何在ubuntu16.04中安装QQ与RTX呢？我折腾了一天，终于圆满解决问题了。RTX的安装会比较麻烦些，QQ则是借助别人打好的包
category: ['效率', 'Linux']
keywords: ubuntu, ubuntu16.04, QQ, RTX, WINE, rtx2015, indicator-systemtray-unity

---

不知不觉间，使用`ubuntu` 当工作机使已经有3个月了，完全熟悉了这种环境后，工作的效率得到不少的提升。除了部分 *office* 文档以外，基本是无痛使用了。图片编辑方面勉强使用 *gimp* 还是可以胜任的。唯一蛋痛之处，天朝境内之痛——`QQ` 与`RTX` 。8G内存的机器，开个*win7* 虚拟机，就只为开这两货，内存飙到将近满负载的状态。企业微信推出了，可以无缝接管RTX的消息，但不支持*linux* 。在这种环境下使用，原本相安无事，工作需要，还得额外再开个虚拟机，机器开始吃不消了……

<!-- more -->         

## 安装QQ

本人使用的系统为`ubuntu 16.04 64bit` ，测试安装之前，我开了个虚拟机，模拟相同的环境来试装，成功无误后再在真实机安装使用。

目前在*ubuntu*下 安装 *QQ* 的方案有好几种

1. ubuntu麒麟上wine-qq
2. 网上别人打包的QQ国际版-qqintel.deb
3. deepin打包的qq
4. Longene Wine QQ

第一个我没试；国际版那个安装使用过，功能简单，界面简洁，多开时只能控制一个，使用时间一长会下线；deepin打包的qq，安装过程非常麻烦，光是折腾那个*crossover* 已经累觉不爱了，你问我为毛不直接上deepin的系统？我个人比较倾向是非修改版的，虽然deepin改得很棒用户体验很好，但我怕对工作有影响，毕竟修改了不少的东东。

最后使用的是`Longene Wine QQ` ，某个社区修改打包的作品，旧版本已经无法使用了，登录时会提示 *该版本太旧，请使用新版登录* 。目前的新版是基于*QQ 7.8* 。

### 安装方法

```shell
# 64位的系统先要添加32位库
sudo dpkg --add-architecture i386
sudo apt-get update
# 可能需要添加下列32位库
sudo apt-get install lib32z1 lib32ncurses5

# 安装下载好的qq包
sudo dpkg -i WineQQ7.8-20151109-Longene.deb

# 卸载deb包
sudo apt remove wine-qq7.8-longeneteam
```

### 已知问题

1. 无法保存密码、自动登录
2. 点击密码输入框有时不能激活，需要多点击几次
3. 程序内选择离线后无法再次上线，需要关闭程序，重新启动
4. 其他很多很多没有测试到的问题
5. 无法发送表情
6. 连续开着QQ达6小时左右，会自动断线，必须Kill掉程序后方可重开

针对登录的问题，我已经习惯了扫码登录，完全不用输入；无法发送表情就有点蛋痛了，没法斗图了……查看别人发送的图片时打开会比较慢……当然优点也有，最大的优点是能够正常使用QQ的大部分功能已经非常棒了。点击链接、面板按钮直接ubuntu的浏览器打开，截图功能也能正常使用，接收文件也正常。双开QQ也没问题噢。

## 安装RTX

安装 *RTX* 这货比较蛋疼，步骤略多……直接上操作方法吧……

```shell
# 安装开发版的wine
sudo add-apt-repository ppa:wine/wine-builds
sudo apt-get update
## 安装wine-devel这货很耗时
sudo apt-get install wine-devel

# 安装winetricks
sudo apt-get install winetricks

# 配置成32位环境，按提示操作
WINEARCH=win32 WINEPREFIX=~/.wine winetricks msxml3 gdiplus riched20 riched30 \
ie6 vcrun6 vcrun2005sp1 allfonts
winetricks -q vcrun6sp6

# ~/.bashrc或者你使用的shell配置文件中添加
export WINEARCH=win32

# 安装rtx2015
WINEARCH=win32 WINEPREFIX=~/.wine wine  rtxclient2015formal.exe
```

安装RTX过程中，如果只报一个 *xxxmenu.dll* 注册失败的错误 ，忽略它，已经成功安装了。如果报了N个 *xx.dll注册失败* 则代表安装失败，请参考文章末尾的链接再试。

成功登录*RTX* 后，记得把`自动状态转换` 给取消掉，另外把面板`自动隐藏` 也取消掉。现在你可以*Enjoy Yourself* 了，哈哈。

等等……且慢……我艹……在*ubuntu unity* 界面上，最小化RTX后，没有系统图标，我艹，这还怎么玩耍？

`BUG`： 无法使用其收发文件……蛋疼啊……

## 任务栏显示软件图标

*Ubuntu Unity* 添加了软件图标白名单，因此部分软件的图标无法在任务栏中显示，幸好国外有大神解决了这个问题。

```shell
# 安装indicator-systemtray-unity
sudo apt-add-repository ppa:fixnix/indicator-systemtray-unity
sudo apt-get update
sudo apt-get install indicator-systemtray-unity

# 安装图形界面设置工具
sudo apt-get install dconf-editor

# 卸载命令，区别普遍的卸载参数
sudo apt-get purge indicator-systemtray-unity
```

安装完毕之后，搜索软件`Dconf-Editor`，在*net > launchpad > indicator > systemtray* 中设置显示图标的位置，慢慢摸索你就懂了。

## 尾巴

无痛无缝使用*RTX* 与 *QQ* 的感觉真他喵的爽……同时把系统负载降低了不少，内存占用这块可以减轻不少……哈哈。

最后要特别吐嘈下流氓公司——渣度，妈蛋，渣度网盘现在非会员下载，直接给你限速，即便用它家的XX网盘管家下载自己的文件，7K/S，我也是醉了……这回是要彻底地和渣度说再见了……

### 参考文章

> [ubuntu RTX安装手记](https://jiangchunyu.github.io/2016/08/27/Ubuntu-%E6%89%8B%E8%AE%B0%E4%B9%8BRTX-%E8%85%BE%E8%AE%AF%E9%80%9A/)
>
> [ubuntu unity 状态栏显示软件图标](http://www.tuicool.com/articles/7VrAn2)
>
> [完美使用deepin QQ](http://www.findspace.name/easycoding/1748)
>
> [Longene Wine QQ](http://www.longene.org/forum/viewtopic.php?f=6&t=30516)