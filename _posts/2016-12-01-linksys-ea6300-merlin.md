---
layout: post
title: Linksys EA6300刷梅林merlin
descriptions: 成功把linksys ea6300 v1刷上梅林merlin固件，卡在cfe miniweb server，过程折腾了不少时间，继续把过程码下来，方便大家吧。
category: 路由器
keywords: linksys, ea6300, ea6300 v1, ea6400, merlin, 梅林
---

自从国庆假期结束时，把 *Linksys EA6300* 刷成 *DD WRT* 固件后，使用起来并没有感觉到一丝地畅快，主要的痛点在于没能实现 *自动翻墙* ，略为郁闷……于是乎这期间把它冷落在一旁，虽然它仍在服役中。适逢家里的某通二级宽带即将到期，加之双十一电信有活动，果断投入电信的大怀抱，啧啧，免费送一年的电信*IPTV* ，这酸爽……不敢想象啊……YY着跳了电信的坑，翻墙时应该会更加畅快吧……翻墙……对了，我艹……ea6300还是没自动翻啊……好像 *梅林* 的固件支持噢。嘿嘿，找到教程了，连续两个晚上下班后折腾，终于搞定了。

<!-- more -->

## 前情提要

开刷之前，先把当前路由器的情况给说清楚，免得直接跟着步骤走，掉坑里都不知道。

上篇文章 [Linksys EA6300刷dd wrt]({{ site.url }}/2016/10/08/linksys-ea6300-dd-wrt.html) 已经把我刷 *dd wrt* 的过程详细描述清楚了，*ea 6300 v1* 你可以直接认为它是 *ea6400* 即可。

我刷完 dd 的固件后，使用过程中，除了不能实现自动翻墙外，其他的功能使用起来也略为繁琐。曾经打算好好熟悉下 *dd* 的详细使用，可折腾没两下就弃坑了。有个周末尝试把 *dd* 升级，一番折腾下来，死活升级不了，要么升级后直接挂掉，硬重置才能救活；要么重启后直接进入 *cfe miniweb server* ，再刷仍然进入旧版的 *dd* 。

心灰意冷中……

电信网络投入使用后，更是心急想把这破路由器给用起来，妈蛋，老子索性不按步骤走，直接在 *dd* 的界面强行刷入 *梅林* 的固件，嘿嘿，居然成功了噢……哈哈，原来就这么简单啊！好吧，把它连接到旧的宽带中，先熟悉下梅林的使用吧……一股雄心壮志顿时从心中升了起来，结果拔电源重开机后，我艹，直接进入  *cfe miniweb server*界面，我了个大艹。一脸懵逼……后来谷歌一番，有网友直言，这种情况就是砖了……

继续心灰意冷……

第二天，又抽了点时间尝试抢救这破路由器，大概罗列了3个方案，如果这3个方案都失效，则证明这货确实砖了，届时将不准备抢救，直接换了，哎……

## 干货要点

如果路由器有意识的话，估计这货唯一的台词便是：我觉得我还可以抢救一下。

下面开始说干货了，赶紧搬好小板凳过来。

刷固件步骤

```txt
1. 确认路由器型号 ea6300 v1
2. 官方固件下恢复出厂设置
3. 官方固件下再升级官方固件
4. 刷入精简版 ddwrt 做过渡
5. 把编辑好的CFE刷入
6. 进入CFE MINI WEBSERVER刷入 梅林固件
7. 重启，享受人生
```

每一步的要点如上所述，详细的操作方法请查看文章末尾的参考链接—— *ea6400详细刷梅林教程* 。如果更新完 *CFE* 信息后，你的路由器仍然能够重启进入系统，恭喜你，证明你的路由器通过考验了。

### TTL信息查看

刷固件过程中，请使用网线连接路由器与计算机，计算机手动设置静态IP

```shell
# linux系统输入
ping 192.168.1.1

# windows系统输入
ping 192.168.1.1 -t
```

学会查看窗口中显现的ping信息，

```shell
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=0.143 ms
64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=0.128 ms
64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=0.128 ms
64 bytes from 10.0.0.1: icmp_seq=4 ttl=64 time=0.141 ms
```

如果 *ttl=64* ，则证明路由器启动完毕，可以正常连接

如果 *ttl=100* 一直显示这玩意，那你就得硬重置了，如无效，嘿嘿，恭喜你中奖了。

通常你刷好固件后，正常的重启过程中 ping 的 ttl 信息不断变化，过程大致为

*无法连接* > ttl=100 > *无法连接*  > ttl=64 > *无法连接*  > ttl=64[持续状态]

### 清除NVRAM

*cfe miniweb server* 是个啥玩意？它相当于电脑里头的 *BIOS* ，掌管着路由器的启动信息之类的吧。那如何清除 *NVRAM* 呢？

```shell
# cfe miniweb server界面
点击 Restore default NVRAM values

# ssh连接到路由器后
nvram erase

# 开机过程中
按住路由器上的 wps 键的同时插电源线
```

### 卡在cfe miniweb server

话说我的破路由器一直开机卡在 *cfe miniweb server* 界面，硬重置亦无效，直接拖 梅林 的固件刷也无效。到Linksys官网下载原版固件，拖上去更新，嘿嘿，路由器可以成功启动进入了。当然进入的仍然是该死的 *DD WRT* 界面，区别是他喵的固件版本号居然更新了，之前刷的终于生效了？

我仔细回想前后两次的刷机过程，卡在 *cfe miniweb server* 的原因估计是当初刷 *dd* 时，没有用官方固件再刷一次，清除掉那个第二分区导致的。

好了，路由器救回来了，恢复出厂设置，刷回精简版的 DD 固件，再刷入 梅林 固件，再在梅林界面中恢复出厂设置，拔电源线重插，确保这回 *ea6300* 真的刷上 梅林 固件了。嘿嘿。

### 固件升级

梅林的固件升级，记得要点选去除 jffs 的设置。

### 怎么关机

路由器上是没有关机键的，那如果老子就是想关机怎么整？

```shell
# ssh 连接到路由器上
halt
```

## 尾巴

总结下来，妈蛋，老天再给一次机会我，我选择不刷固件了……心好累……

还是那句话，在未搞懂教程前，莫盲目开刷。有些教程没交待清楚环境，盲目跟刷，风险很大。

我刷的这个 梅林，是*koolshare* 论坛上的牛人制作出来的，正确的说应该是华硕界面+梅林的功能，在此表示感谢。刷了固件后，路由器温度维持在 46 度左右，啧啧。

下回再换路由器，估计得败一个华硕的了……

参考链接

> [固件下载页](http://firmware.koolshare.cn/)
>
> [完整版 与 精简版的切换](http://koolshare.cn/forum.php?mod=viewthread&tid=65343&extra=page%3D1%26filter%3Dtypeid%26typeid%3D16)
>
> [ea6400 详细刷梅林教程](http://koolshare.cn/forum.php?mod=viewthread&tid=9422&highlight=EA6400%2B%E5%85%A8%E7%B3%BB%E7%BB%9F%E5%85%BC%E5%AE%B9CFE%2B378.57)
