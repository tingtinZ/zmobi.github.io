---
layout: post
title: Ubuntu色温调节
category: Linux
description: ubuntu下使用f.lux作色温调节，如何设置固定的色温，不随着时间变化而变化呢？
keywords: ubuntu, color temperature, flux, f.lux, 色温, 色温调节
---

自从生产环境迁移至ubuntu之后，感觉整个人都精神了，吃饭也香了，一口气能爬5楼了，呵呵。

你说那么多就是为了装逼……

这位同学，我装逼的时候，请安静好吗？

起始对色温这玩意没啥概念，偶然的一个机会看到某个软件网站上有推荐f.lux，试用了一番，嘿嘿，果然好使。
<!-- more -->

`f.lux`，网络上查找时亦可写成*flux*，国外开发的免费色温调节软件，可以*根据地理位置，随着白天与晚上的变化自动调节设备的色温*，设备包括手机、平板、电脑。
平台支持方面： *linux*、*MacOS*、*android*、*ios* 均支持，其中ios需要越狱方可使用。


iphone用户们不用慌，鸡贼的苹果早已把这玩意抄到IOS上，美曰其名「改头换面」叫 *night shit*。


回归本文的槽点吧，之前在*瘟系统*下用着好好地，可以自定义*daytime*白天色温和*nighttime*夜晚色温，可换到ubuntu之后，居然无法自定义了。如下图所示

<img src="/res/img/in_posts/flux-setting.png">

只能设置经纬度，白天的色温由经纬度决定；`nighttime color temperature`一栏可供选择的仅为夜晚色温。怎么办呢？急死爹了。

鉴于所使用的显示器太渣，色温不常开个**2700K**，分分钟亮瞎哥的眼睛。

到官网查询下文档呗，结果没官方文档……于是到论坛逛了下，某个国外网友有同样的想法，想要固定白天色温值，官方人员回答说，软件本身不支持这种设置。
幸好有另外一个鸡智的网友，提供了个智取的解决方案，把`经纬度设置成北极或者南极`，根据当前季节选择，每半年更换一次即可。图片里设置的是南极经纬度。

哈哈，完美解决啊……看着面前这屎黄屎黄的屏幕，哥终于能够安心的挊代码了……

最后，吐槽下感受，Ubuntu下使用virutalbox开个WIN7挂着QQ和RTX，丝毫不影响整机流畅性，比win7用着爽太多了。
